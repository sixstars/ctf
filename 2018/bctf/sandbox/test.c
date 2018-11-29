#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(){
    write(0,0,0);
    read(-1,0,0);
    printf("%p\n",*(long*)0x601028);
    printf("%p\n",*(long*)0x601018);
    exit(0);
}

