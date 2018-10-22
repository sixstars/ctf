/*
 * main.c
 * Copyright (C) 2018 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <string.h>
int main(int argc, char *argv[]){
    printf("%p%p%p%p%p%p%p%p%p%p%p",alarm,system,
            printf,sleep,execve,exit,strdup,exit,malloc,free,calloc,puts
            ,read,write,close,mmap,fprintf,fopen,fclose,fscanf);
    return 0;
}
