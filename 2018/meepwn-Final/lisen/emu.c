/*
 * emu.c
 * Copyright (C) 2018 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */


#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>

#include <sys/stat.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#define uint_8 unsigned char
#define ELF_ADD (0x100000)


void loadfile(){
    int fd=open("./bin",O_RDWR);
    off_t size=lseek(fd,0,SEEK_END);
    mmap((void*)ELF_ADD,size,PROT_READ|PROT_WRITE|PROT_EXEC,MAP_PRIVATE,fd,0);
    close(fd);
}


int main(){
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setvbuf(stderr,0,2,0);
    loadfile();
	asm(
        "push $0x1000da\n"
        "pop %rax\n"
        "call %rax\n"
	);
	return 0;
}

