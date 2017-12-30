/*
  The s-box is linear and so with the whole encryption.
  Set a variable for each bit of key, we can calculate the linear combinations between plain and cipher text
  I choose to get the plain->cipher mapping and bruteforce the missed plaintext. However using cipher-plain mapping would be much more elegant
  Since this solution is not good enough I omit the full scripts here. This cpp file is for mapping calculation.
*/

#include<iostream>
#include <inttypes.h>
#include<stdio.h>
#include<stdint.h>

using namespace std;

struct state {
    uint64_t high;
    uint64_t low;
    uint8_t con;
};

const int nrounds=31337;

state keys[(nrounds+1)*16][8];

void add(state x[], state y[], state r[]) {
    for (int i=0;i<8;i++) {
        r[i].high = x[i].high^y[i].high;
        r[i].low = x[i].low^y[i].low;
        r[i].con = x[i].con^y[i].con;
    }
}
void addeq(state x[], state r[]) {
    for (int i=0;i<8;i++) {
        r[i].high ^= x[i].high;
        r[i].low ^= x[i].low;
        r[i].con ^= x[i].con;
    }
}
void sets(state x[], state r[]) {
    for (int i=0;i<8;i++) {
        r[i].high = x[i].high;
        r[i].low = x[i].low;
        r[i].con = x[i].con;
    }
}

void addi(state x[], int y) {
    int tmp=1;
    for (int i=7;i>=0;i--) {
        if (y&tmp)
            x[i].con^=1;
        tmp<<=1;
    }
}
void seti(state x[], int y) {
    int tmp=1;
    for (int i=7;i>=0;i--) {
        if (y&tmp)
            x[i].con=1;
        tmp<<=1;
    }
}

void mul2(state x[], state r[]) {
    for (int i=0;i<7;i++) {
        r[i].high=x[i+1].high;
        r[i].low=x[i+1].low;
        r[i].con=x[i+1].con;
    }
    r[7].high=x[0].high;
    r[7].low=x[0].low;
    r[7].con=x[0].con;
    r[6].high^=x[0].high;
    r[6].low^=x[0].low;
    r[6].con^=x[0].con;
    r[4].high^=x[0].high;
    r[4].low^=x[0].low;
    r[4].con^=x[0].con;
    r[3].high^=x[0].high;
    r[3].low^=x[0].low;
    r[3].con^=x[0].con;
}
void mul3(state x[], state r[]) {
    state tmp[8];
    mul2(x, tmp);
    add(x,tmp,r);
}

int trans[] = {343 , 427 , 212 , 106 , 354 , 487 , 499 , 174};

void sbox(state x[], state r[]) {
    state tmp;
    for (int i=0;i<8;i++) {
        tmp.high=0;
        tmp.low=0;
        tmp.con=0;
        int tmpt=trans[i];
        if (tmpt&1)
            tmp.con=1;
        for (int j=7;j>=0;j--) {
            tmpt/=2;
            if (tmpt&1) {
                tmp.high ^= x[j].high;
                tmp.low ^= x[j].low;
                tmp.con ^= x[j].con;
                //printf("%d: %d->%d\n",j, x[j].con,tmp.con);
            }
        }
        r[i].high=tmp.high;
        r[i].low=tmp.low;
        r[i].con=tmp.con;
    }
}

void init_key() {
    for (int i=0;i<8;i++) 
        for (int j=0;j<8;j++) {
            int tmp = 63-(i*8+j);
            keys[i][j].high = ((uint64_t)1<<tmp);
            keys[i][j].low = 0;
            keys[i][j].con = 0;
        }
    for (int i=8;i<16;i++) 
        for (int j=0;j<8;j++) {
            int tmp = 63-((i-8)*8+j);
            keys[i][j].low = ((uint64_t)1<<tmp);
            keys[i][j].high = 0;
            keys[i][j].con = 0;
        }
}

void expand_key() {
    state word[4][8];
    int rcon=0x8d;
    for (int i=1;i<=nrounds;i++) {
        int base=i*16;
        sbox(keys[base-4],word[3]);
        sbox(keys[base-3],word[0]);
        sbox(keys[base-2],word[1]);
        sbox(keys[base-1],word[2]);
        addi(word[0],rcon);
        rcon<<=1;
        if (rcon&0x100) {
            rcon&=0xff;
            rcon^=0x1b;
        }
        for (int j=0;j<4;j++)
            add(word[j],keys[base+j-16],keys[base+j]);
        for (int j=4;j<16;j++)
            add(keys[base+j-4],keys[base+j-16],keys[base+j]);
    }
}

void doout(state x) {
    uint64_t tmp=((uint64_t)1<<63);
    for (int i=63;i>=0;i--) {
        if (tmp&x.high)
            printf("1");
        else
            printf("0");
        tmp>>=1;
    }
    tmp=((uint64_t)1<<63);
    for (int i=63;i>=0;i--) {
        if (tmp&x.low)
            printf("1");
        else
            printf("0");
        tmp>>=1;
    }
    if (x.con)
        printf("1\n");
    else
        printf("0\n");
}

void do_test() {
    addi(keys[16],231);
    for (int i=0;i<8;i++)
        doout(keys[16][i]);
    mul3(keys[16],keys[17]);
    for (int i=0;i<8;i++)
        doout(keys[17][i]);
}

int plain[16]={0, 0, 0, 0, 0, 0, 0, 16, 51, 52, 67, 51, 95, 71, 71, 71};
state cur[16][8];

void subbytes() {
    state tmp[8];
    for (int i=0;i<16;i++) {
        sets(cur[i], tmp);
        sbox(tmp, cur[i]);
    }
}

void shiftrows() {
    state tmp[8];
    sets(cur[1],tmp);
    sets(cur[5],cur[1]);
    sets(cur[9],cur[5]);
    sets(cur[13],cur[9]);
    sets(tmp,cur[13]);

    sets(cur[2],tmp);
    sets(cur[10],cur[2]);
    sets(tmp,cur[10]);
    sets(cur[6],tmp);
    sets(cur[14],cur[6]);
    sets(tmp,cur[14]);

    sets(cur[3],tmp);
    sets(cur[15],cur[3]);
    sets(cur[11],cur[15]);
    sets(cur[7],cur[11]);
    sets(tmp,cur[7]);
}

void mixcolumns() {
    state val[4][8];
    state tmp[8];
    state tmp3[8];
    for (int i=0;i<4;i++) {
        int base=i*4;
        for (int j=0;j<4;j++)
            sets(cur[base+j],val[j]);

        mul2(val[0], tmp);
        mul3(val[1], tmp3);
        addeq(tmp3,tmp);
        addeq(val[2],tmp);
        addeq(val[3],tmp);
        sets(tmp,cur[base]);

        mul2(val[1], tmp);
        mul3(val[2], tmp3);
        addeq(tmp3,tmp);
        addeq(val[0],tmp);
        addeq(val[3],tmp);
        sets(tmp,cur[base+1]);

        mul2(val[2], tmp);
        mul3(val[3], tmp3);
        addeq(tmp3,tmp);
        addeq(val[0],tmp);
        addeq(val[1],tmp);
        sets(tmp,cur[base+2]);

        mul2(val[3], tmp);
        mul3(val[0], tmp3);
        addeq(tmp3,tmp);
        addeq(val[1],tmp);
        addeq(val[2],tmp);
        sets(tmp,cur[base+3]);
    }
}

void addkey(int round) {
    int base=round*16;
    for (int i=0;i<16;i++)
        addeq(keys[base+i], cur[i]);
}

void encrypt_block() {
    addkey(0);
    for (int i=1;i<nrounds;i++) {
        subbytes();
        shiftrows();
        mixcolumns();
        addkey(i);
    }
    subbytes();
    shiftrows();
    addkey(nrounds);
}

int main() {
    init_key();
    //do_test();
    expand_key();
    {
        scanf("%d", plain+7);
        scanf("%d", plain+13);
        scanf("%d", plain+14);
        scanf("%d", plain+15);
        for (int i=0;i<16;i++)
            seti(cur[i],plain[i]);
        encrypt_block();
    }
    for (int i=0;i<16;i++)
        for (int j=0;j<8;j++)
            doout(cur[i][j]);
    return 0;
}
