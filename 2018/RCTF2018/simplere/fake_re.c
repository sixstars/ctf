/*
 * re.c
 * Copyright (C) 2018 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
#define uint unsigned int
#define ulong unsigned long long
unsigned char buf[0x24];
uint fun(uint* array,int len,int *dev){
    uint N=0;
    uint bk;
    uint fd;
    int p;
    int idx;
    for(int i=0x34/len+6;i;i--){
        bk=array[len-1];
        idx=0;
        N-=0x61C88647;
        p=(N>>2)&3;
        while(len-1>idx){
            fd=array[idx+1];
            array[idx]+=((fd^N)+(bk^dev[p^idx&3]))^(((fd<<2)^(bk>>5))+((fd>>3)^(bk<<4)));
            bk=array[idx++];
        }
        array[len-1]+=((array[0]^N)+(bk^dev[p^idx&3])) ^ (((array[0]<<2)^(bk>>5))+((array[0]>>3)^(bk<<4)));
    }
    return N;
}

void def_fun(uint* array,int len,int *dev,uint N){
    int p;
    int idx;
    uint fd,bk;
    for(int i=0x34/len+6;i;i--){
        p=(N>>2)&3;
        fd=array[0];
        idx=len-1;
        while(idx>0){
            bk=array[idx-1];
            array[idx]-=((fd^N)+(bk^dev[p^idx&3]))^(((fd<<2)^(bk>>5))+((fd>>3)^(bk<<4)));
            fd=array[idx];
            idx--;
        }
        bk=array[len-1];
        array[0]-=((fd^N)+(bk^dev[p^idx&3]))^(((fd<<2)^(bk>>5))+((fd>>3)^(bk<<4)));
        N+=0x61C88647;
    }
}

int main(){
    int array[]={
        0x67452301,
        0xefcdab89,
        0x98badcfe,
        0x10325476
    };
    
    for(int len=0x20;len>0;len--){
        uint N=fun((uint*)buf,len>>2,array);
        memset(buf,0,0x24);
        memcpy(buf,"quehsj_kcneop_amneuf_ieha_ehdhde",0x20);
        def_fun((uint*)buf,len>>2,array,N);
        puts(buf);
    }
    return 0;
}


