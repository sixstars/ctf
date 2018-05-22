/*
 * re.c
 * Copyright (C) 2018 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

#include <stdio.h>
#include <stdlib.h>

#define uint unsigned int
#define ulong unsigned long long

uint (*ptr)(uint,ulong,int,int,int);

int main(){
	uint array[]={0xB80C91FE,0x70573EFE,0xBEED92AE,0x7F7A8193,
		0x7390C17B,0x90347C6C,0xAA7A15DF,0xAA7A15DF,0x526BA076,
		0x153F1A32,0x545C15AD,0x7D8AA463,0x526BA076,0xFBCB7AA0,
		0x7D8AA463,0x9C513266,0x526BA076,0x6D7DF3E1,0xAA7A15DF,
		0x9C513266,0x1EDC3864,0x9323BC07,0x7D8AA463,0xFBCB7AA0,
		0x153F1A32,0x526BA076,0xF5650025,0xAA7A15DF,0x1EDC3864,0xB13AD888,};
	ulong N=0x1d082c23a72be4c1;

    FILE *f=fopen("./re.bin","r");

    char *buf=(char*)malloc(0x2000);
    int idx=0;
    while(1){
    	int n=fread(buf+idx,1,0x1000,f);
    	if(n <=0){
    		break;
    	}
    	idx+=n;
    }
    
    ptr=(uint (*)(uint,ulong,int,int,int))buf;

    for(int i=0;i<30;i++){
	    for(int j=0;j<0x100;j++){
	        if(ptr(j,N,0,0,0) == array[i]){
	        	printf("%c",j);
	        	break;
	        }
	    }
    }

	return 0;
}
