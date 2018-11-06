#include <stdio.h>
#include <stdlib.h>
const char *ptr="0123456789abcdef";
int main(){
    srand(300);
    char tmp[0x21]={0};
    for(int i=0;i<0x20;i++){
        tmp[i]=ptr[rands(0x10)];
    }
    puts(tmp);
}
