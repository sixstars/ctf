#include <unistd.h>
struct linux_dirent {
   long           d_ino;
   off_t          d_off;
   unsigned short d_reclen;
   char           d_name[];
};
int main(int argc,char *a[],char *env[]){
    int fd=open("./",0);
    struct linux_dirent fs[10];
    syscall(0x4e,fd,&fs,1000);
}
