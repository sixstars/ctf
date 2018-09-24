
#define _POSIX_C_SOURCE 1
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

void greet(FILE *in, FILE *out)
{
    char buf[0x40];
    printf("Enter username: ");
    read(fileno(in), buf, 0x40);
    fprintf(out, "Hey %s", buf);
}

int num()
{
    static char buf[0x10];
    read(fileno(stdin), buf, 0x10);
    return atoi(buf);
}

int main()
{
    int len;
    char buf[0x40];

    setbuf(stdout, NULL);

    greet(stdin, stdout);
    sleep(1);

    printf("Enter length: ");
    if (0x40 <= (len = num())) {
        printf("No!\n");
        exit(1);
    }

    printf("Enter string (length %u): ", len);
    read(fileno(stdin), buf, len);
    printf("Thanks, bye!\n");
}

