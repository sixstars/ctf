/*
 * run.c
 * Copyright (C) 2019 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>

#include <sys/stat.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>
#include <stdint.h>
#define uint_8 unsigned 
#define ELF_ADD 0x100000
void loadfile(char* name){
    FILE* fd = fopen(name,"r");
    fseek(fd,0,SEEK_END);
    uint64_t size = ftell(fd);
    fseek(fd,0,SEEK_SET);
    mmap((void*)ELF_ADD,(size+0xfff)&0xfffff000,PROT_READ|PROT_WRITE|PROT_EXEC,MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS,-1,0);
    uint64_t pc=0;
    while(1){
        uint64_t t = fread(ELF_ADD+pc,0x1,0x100,fd);
        if (t<=0)
            break;
        pc+=t;
    }
}

uint8_t* locate_call(uint8_t *ptr){
    for(int i=0;i<0x1000;i++){
        if(ptr[i] == 0xe8 && ptr[i+5] == 0x90){
            return &ptr[i];
        }
    }
}
static int hit = 0;
static void (*next_addr)(uint8_t,uint8_t,uint8_t);
static uint8_t data[3];

static uint32_t b;

void gdb(uint64_t a,uint64_t b,uint64_t c){
    uint8_t *p = (uint8_t*) *(uint64_t*)(c+0xa8);
    p[0] = 0xc9;
    p[1] = 0xc3;
    hit = 1;
}

void prog_init(){
    struct sigaction s;
    s.sa_handler = (__sighandler_t) gdb;
    s.sa_flags = SA_NODEFER;
    sigfillset(&s.sa_mask);
    sigaction(SIGSEGV, &s, 0);
}
uint8_t* find_jnz(uint8_t* pc){
    while(1){
        if(pc[0] == '\x75')
            break;
        pc++;
    }
    return pc;
}
int main(int argc,char* argv[],char*envp[]){
    loadfile(argv[1]);
    setvbuf(stdout,0,2,0);
    prog_init();
    for(int cnt = 0;cnt<0x10;cnt++){
        uint32_t off;
        scanf("%d",&off);
        next_addr = (off + ELF_ADD)&0xffffffff;
        uint8_t* record = next_addr;
        //next_addr = (void (*)(uint8_t))(0x190D03+ELF_ADD);
        memset(data,0,sizeof(data));
        for(int i=0;i<3;i++){
            uint8_t *hlt_pc = find_jnz(record)+2;
            uint64_t orgin = *(uint64_t*)hlt_pc;
            *(uint64_t*)hlt_pc = 72057594057131206;// mov[1],1
            int tmp_cnt = 0;
            for(;!hit && tmp_cnt<0x100;tmp_cnt++){
                next_addr(data[0],data[1],data[2]);
                data[i]++;
            }
            if(tmp_cnt == 0x100){
                printf("not found!\n");
                exit(0);
            }
            *(uint64_t*)hlt_pc = orgin;
            record = hlt_pc;
            data[i]--;
            hit = 0;
        }
        printf("%02x%02x%02x",data[0],data[1],data[2]);
    }
    printf("\n");
}







