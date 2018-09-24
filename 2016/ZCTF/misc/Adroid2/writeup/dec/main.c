#include <stdio.h>
#include <string.h>

char enc[0x1460] = {};
char dec[0x1460] = {};

int main(int argc, char **argv, char **envp) {
    int dl = dlopen("/data/local/tmp/libJNIclass.so", 1);
    if (!dl) {
        printf("dlopen error!\n");
        return 1;
    }
    void (*f)(char*, int, char *, char *) = dlsym(dl, "DES_Decrypt");
    if (!f) {
        printf("dlsym error\n");
        return 2;
    }
    FILE* fp = fopen("./cipher", "rb");
    fread(enc, 1, 0x1460, fp);
    close(fp);
    // printf("enc len = %d\n", strlen(enc));
    f(enc, 0x1460, "{Notthis", dec);
    fp = fopen("./xxx.png", "wb");
    fwrite(dec, 1, 0x1460, fp);
    close(fp);
    return 0;
}
