/*
 * re.c
 * Copyright (C) 2018 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
uint32_t fast_power(uint32_t x, uint32_t p, uint32_t N) {
    uint64_t s = 1;
    uint64_t a1 = x;
    uint32_t a2=p;
    while(a2) {
        if(a2 & 1)
            s = s * a1 % N;
        a1 = a1 * a1 % N;
        a2 = a2 >> 1;
    }
    return s;
}

uint16_t trans(uint16_t a, uint16_t a2) {
    uint16_t v2;
    uint16_t i;
    for(i = a2; i & a; i = 2 * (i & v2)) {
        v2 = a;
        a ^= i;
    }
    return i | a;
}
int main() {
    char flag[0x22]="6o_M@ny_an7i_Rev3rsing_Techn1111s";
    /*
    uint32_t dev[]={0x556E4969,0x2E775361,0x893DAE7,0x96990423,0x6CF9D3E9,0xA505531F};
    uint32_t result[]={0x54A0B9BD,0x4B818640,0x8EB63387,0xA9EABEFD,0xB8CDF96B,0x113C3052};
    for (int idx=0;idx<6;idx++){
        for(uint32_t i=0;i<0xffffffff;i++){
            if(dev[idx]*i==result[idx]){
                *((uint32_t*)flag+idx)=i;
                puts(flag);
            }
        }
    }
    */
    uint32_t p=*((uint32_t*)flag+6);
    uint16_t i=0;
    while(i<0xffff){
        if(fast_power(p,i,0xF64BB17D)==0x6F82C8DC){
            *((uint16_t*)flag+14)=i;
            uint16_t j=0;
            while(j<0xffff){
                if(trans(i,j)==0xA496){
                    *((uint16_t*)flag+15)=j;
                    puts(flag);
                }
                j++;
            }
        }
        i++;
    }
    return 0;
}
