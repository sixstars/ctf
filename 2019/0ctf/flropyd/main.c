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
uint64_t cnt;
void load_table(){
    int fd = open("./table",0);
    table = malloc(4096*8);
    read(fd,&cnt,8);
    read(fd,table,cnt * cnt * 8);
}
int main(int argc, char *argv[]){
    load_table();
    for(int i=0;i<cnt;i++){
        for(int j=0;j<cnt;j++){
            for(int k=0;k<cnt;k++){
                if( table[(j<< 6) + k] > table[(j<<6) + i] + table[(i<<6) + k]  ){
                    table[(j<< 6) + k] = table[(j<<6) + i] + table[(i<<6) + k];
                }
            }
        }
    }
    for(int i=0;i<cnt*cnt;i++){
        printf("0x%d %lu\n",i,table[i]);
    }
    return 0;
}




