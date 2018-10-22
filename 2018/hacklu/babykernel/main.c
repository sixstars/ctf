/*
 * main.c
 * Copyright (C) 2018 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

#include <stdio.h>
#include <stdlib.h>
int main(int argc, char *argv[]){
	int id;
    printf("input id:");
	scanf("%d",&id);
    setuid(id);
    return 0;
}
