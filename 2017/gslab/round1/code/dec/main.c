#include <stdio.h>
#include <string.h>

char rsa[0x10000] = {};

int main(int argc, char **argv, char **envp) {
    int dl = dlopen("/data/local/tmp/libnative-lib.so", 1);
    if (!dl) {
        printf("dlopen error!\n");
        return 1;
    }
    void (*f)(void *) = dlsym(dl, "_ZN3RSAC2Ev");
    if (!f) {
        printf("dlsym error\n");
        return 2;
    }
    void (*f_key)(void *, unsigned int) = dlsym(dl, "_ZN3RSA6RSAKeyEj");
    if (!f_key) {
        printf("dlsym error\n");
        return 2;
    }
    // void (*f_dec)(void *, unsigned int) = dlsym(dl, "_ZN3RSA6RSAKeyEj");
    // if (!f_key) {
    //     printf("dlsym error\n");
    //     return 2;
    // }

    unsigned int seed;
    scanf("%u", &seed);
    printf("%u\n", seed);
    f(rsa);
    f_key(rsa, seed);

    return 0;
}
