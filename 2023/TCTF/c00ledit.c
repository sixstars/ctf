#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <sys/unistd.h>

typedef struct
{
    long size;
    char *buf;
} node_t;

node_t *node_list[0x10] = {0};

void show_menu()
{
    puts("1. add");
    puts("2. delete");
    puts("3. edit");
    puts("4. show");
    puts("5. exit");
    printf("Your choice: ");
}

long get_long()
{
    char tmp[8];
    memset(tmp, 0, sizeof(tmp));
    read(0, tmp, sizeof(tmp));
    return atol(tmp);
}

void do_add()
{
    static int node_count = 0;
    if (node_count >= sizeof(node_list) / sizeof(node_list[0]))
    {
        puts("Enough!");
        return;
    }
    node_list[node_count] = (node_t *)malloc(sizeof(node_t));
    node_list[node_count]->size = 0x1000;
    node_list[node_count]->buf = malloc(0x1000);
    if (!node_list[node_count]) {
        perror("malloc");
        exit(-1);
    }
    printf("Current node: %d\n", node_count);
    ++node_count;
    return;

    // long idx = get_long();
    // if (idx >= 0 && idx < sizeof(node_list) / sizeof(node_list[0]))
    // {
    //     node_list[idx] = (node_t *)malloc(sizeof(node_t));
    //     node_list[idx]->size = 0x1000;
    //     node_list[idx]->buf = malloc(0x1000);
    //     if (!node_list[idx]->buf)
    //     {
    //         perror("malloc");
    //         exit(-1);
    //     }
    // }
    // else
    // {
    //     puts("Invalid!");
    // }
}

void do_edit()
{
    static int edit_count = 0;
    if (edit_count > 16)
    {
        puts("No chance!");
        return;
    }
    printf("Index: ");
    long idx = get_long();
    if (!node_list[idx]) {
        puts("Invalid index!");
        return;
    }
    printf("Offset: ");
    long offset = get_long();
    if (offset + 8 > node_list[idx]->size) {
        puts("Invalid offset!");
        return;
    }
    printf("Content: ");
    read(0, node_list[idx]->buf+offset, 8);
    ++edit_count;
    return;
}

int main()
{
    for (;;)
    {
        show_menu();
        long choice = get_long();
        switch (choice)
        {
        case 1:
            do_add();
            break;
        case 2:
            puts("Not implemented!");
            break;
        case 3:
            do_edit();
            break;
        case 4:
            puts("Not implemented!");
            break;
        case 5:
            return 0;
        default:
            goto fail;
        }
    }
fail:
    puts("invalid choice");
    return -1;
}

__attribute__((constructor)) void init()
{
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}
