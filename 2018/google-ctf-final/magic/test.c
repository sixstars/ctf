/*
 * main.c
 * Copyright (C) 2018 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>

#include "file.h"
//const char *file="flag.mgc";
const char *file="1.mgc";

int main(int argc, char *argv[]){
    struct stat st;
    stat(file,&st);
    size_t len=st.st_size;
    int fd=open(file,0);
    char *ptr=malloc(len);
    if(read(fd,ptr,len)!=len){
        exit(1);
    }
    struct magic *mg=(struct magic *)ptr;
    size_t size = len/sizeof(struct magic);
    for(int i=1;i<size;i++){
        printf("cont_level: %d\t",mg[i].cont_level);
        printf("reln:%c, factor:%d\t",mg[i].reln,mg[i].factor);
        printf("vallen: %d,flag: %d\t",mg[i].vallen,mg[i].flag);
        printf("type: %d,in_type: %d\t",mg[i].type,mg[i].in_type);
        printf("in_op: %d,mask_op: %d\t",mg[i].in_op,mg[i].mask_op);
        printf("cond: %d,factor_op:%d,offset: %d,lineno:%d\t",mg[i].cond,mg[i].factor_op,mg[i].offset,mg[i].lineno);
        printf("desc: %s,",mg[i].desc);
        printf("value:%d,%s\n",mg[i].value.b,mg[i].value.hs);
    }
    puts("");
    printf("total: %d\n",size);
    return 0;
}
