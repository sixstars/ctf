/*
 * main.c
 * Copyright (C) 2018 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

#include <stdio.h>
#include <stdlib.h>
int main(int argc, char *argv[]){
    char c;
    read(0,&c,0x100000000);
    srand(time(0)+atoi(argv[1]));
    printf("%d\n",rand());
    return 0;
}
