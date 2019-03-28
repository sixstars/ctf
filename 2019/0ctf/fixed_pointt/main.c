/*
 * main.c
 * Copyright (C) 2019 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <string.h>
uint64_t *table;
void load_table(){
    int fd = open("./table",0);
    table = malloc(0x1000);
    if(read(fd,table,0x1000) != 0x1000){
        printf("read fail\n");
        exit(0);
    }
}
int sum(uint64_t x){
    int sum=0;
    while(x){
        if(x&1)
            sum++;
        x>>=1;
    }
    return sum;
}
void reverse(uint8_t* buf,int len){
    uint64_t s,t;
    s=0xffffffffffffffff;
    t=0xffffffffffffffff;
    for(int i=0;i<len;i++){
        uint64_t* ptr = &table[(buf[i]^(s&0xff))*2];
        s = (s >> 8)|((t&0xff)<<56);
        t = t >> 8;
        s = s^ptr[0];
        t = t^ptr[1];
    }
    printf("%lx,%lx\n",s,t);
}
int search_bytes(uint8_t x,int column){
    int d=0;
    if( column >= 8 ){
        column -=8;
        d=1;
    }
    uint8_t *ptr = ((uint8_t*)&table[d])+column;
    for(int i=0;i<0x100;i++){
        if(*ptr == x)
            return i;
        ptr +=0x10;
    }
    return -1;
}
int main(int argc, char *argv[]){
    load_table();
    uint8_t buf[22];

    memcpy(buf,"flag{",5);
    memset(&buf[5],'\xaa',16);
    buf[21] = '}';
    
//    reverse(buf,22);
//    for(int r=21;r>=0;r--){
    int r=21;
    int mark=1;
    uint8_t fake_N[0x10];
    for(uint32_t guess=0;guess<0x100;guess++){
        int idx = search_bytes(guess,21-r);
        if(idx == -1 ){
            printf("guess wrong\n");
            continue;
        }
        idx = idx ^ buf[r];
        fake_N[0] = guess;
        uint8_t *ptr = &table[idx*2];
        for(int pos=0;pos<15;pos++){
            fake_N[pos+1] = ptr[pos] ^ fake_N[pos];
        }
        printf("%lx,%lx\n",*(uint64_t*)fake_N,*(uint64_t*)(fake_N+8));
        if(!memcmp(fake_N,ptr,0x10)){
            printf("Found it\n");
            exit(0);
        }

    }

  //  }
    return 0;
}




