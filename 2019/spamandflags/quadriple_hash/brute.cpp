#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <assert.h>
#include <sys/types.h>
#include<map>

using namespace std;
 
#define LEFTROTATE(x, c) (((x) << (c)) | ((x) >> (32 - (c))))
uint32_t r[] = {7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
                4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21};
uint32_t k[] = {
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
    0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
    0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
    0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
    0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
    0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
    0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
    0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
    0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391};

uint32_t hash_block(const uint32_t *w, uint32_t data, int which_alg) {
  uint32_t a = 0x67452301, b = 0xefcdab89, c = 0x98badcfe, d = 0x10325476;
  switch(which_alg) {
    case 0: a=data;break;
    case 1: b=data;break;
    case 2: c=data;break;
    case 3: d=data;break;
    default: assert(0);
  }
  for(int i = 0; i<64; i++) {
    uint32_t f, g;
    if (i < 16) {
        f = (b & c) | ((~b) & d);
        g = i;
    } else if (i < 32) {
        f = (d & b) | ((~d) & c);
        g = (5*i + 1) % 16;
    } else if (i < 48) {
        f = b ^ c ^ d;
        g = (3*i + 5) % 16;          
    } else {
        f = c ^ (b | (~d));
        g = (7*i) % 16;
    }
    uint32_t temp = d;
    d = c;
    c = b;
    b = b + LEFTROTATE((a + f + k[i] + w[g]), r[i]);
    a = temp;
  }
  switch(which_alg) {
    case 0: return data+a;
    case 1: return data+b;
    case 2: return data+c;
    case 3: return data+d;
    default: assert(0);
  }
}

uint32_t starting_state(int which_alg) {
  switch(which_alg) {
    case 0: return 0x67452301;
    case 1: return 0xefcdab89;
    case 2: return 0x98badcfe;
    case 3: return 0x10325476;
    default: assert(0);
  }
}
 
uint32_t hash_full(const uint8_t* initial_msg, size_t initial_len, int which_alg) {
  int new_len;
  for(new_len = initial_len*8 + 1; new_len%512!=448; new_len++);
  new_len /= 8;
  uint8_t *msg;
  msg = (uint8_t*)calloc(new_len/4 + 64/4, 4);
  memcpy(msg, initial_msg, initial_len);
  msg[initial_len] = 128;
  uint32_t bits_len = 8*initial_len;
  memcpy(msg + new_len, &bits_len, 4);
  uint32_t data = starting_state(which_alg);
  for(int offset=0; offset<new_len; offset += (512/8))
    data = hash_block((uint32_t*)(msg+offset), data, which_alg);
  free(msg);
  return data;
}

const int C=19;
char buffer[1000001];
char buf00[C*C*C+1][100];
char buf01[C*C*C+1][100];
char buf10[C*C+1][64*C+1];
char buf11[C*C+1][64*C+1];
char buf20[C+1][64*C*C+1];
char buf21[C+1][64*C*C+1];
char buf30[1][64*C*C*C+1];
char buf31[1][64*C*C*C+1];

map<uint32_t,uint32_t> d;
map<uint32_t,uint32_t>::iterator it;

const char *s0 = "apple,";
const char *s1 = "cider,";
const char *s2 = "bear,";
const char *s3 = "deer,";
const char *s4 = "elite,";
const char *ss;
long sz,sz1;

void cons0(long cur0) {
    if (cur0<78732) {
        for (int j=0; j<11; j++) {
            if (j>=9) {
                if (cur0%2==0)
                    ss = s2;
                else
                    ss = s3;
                memcpy(buffer+9+j*5, ss, 5);
                cur0 /= 2;
                
            } else {
                if (cur0%3==0)
                    ss = s0;
                else if (cur0%3==1)
                    ss = s1;
                else
                    ss = s4;
                memcpy(buffer+j*6, ss, 6);
                cur0 /= 3;
            }
        }
    } else if (cur0 < 157464){
        cur0 -= 78732;
        for (int j=0; j<11; j++) {
            if (j<2) {
                if (cur0%2==0)
                    ss = s2;
                else
                    ss = s3;
                memcpy(buffer+j*5, ss, 5);
                cur0 /= 2;
                
            } else {
                if (cur0%3==0)
                    ss = s0;
                else if (cur0%3==1)
                    ss = s1;
                else
                    ss = s4;
                memcpy(buffer+j*6-2, ss, 6);
                cur0 /= 3;
            }
        }
    } else if (cur0<236196) {
        cur0 -= 157464;
        for (int j=0; j<11; j++) {
            if (j==0) {
                if (cur0%3==0)
                    ss = s0;
                else if (cur0%3==1)
                    ss = s1;
                else
                    ss = s4;
                memcpy(buffer, ss, 6);
                cur0 /= 3;
            } else if (j<3) {
                if (cur0%2==0)
                    ss = s2;
                else
                    ss = s3;
                memcpy(buffer+j*5+1, ss, 5);
                cur0 /= 2;
            } else {
                if (cur0%3==0)
                    ss = s0;
                else if (cur0%3==1)
                    ss = s1;
                else
                    ss = s4;
                memcpy(buffer+j*6-2, ss, 6);
                cur0 /= 3;
            }
        }
    } else {
        cur0 -= 236196;
        for (int j=0; j<11; j++) {
            if (j==0) {
                if (cur0%2==0)
                    ss = s2;
                else
                    ss = s3;
                memcpy(buffer, ss, 5);
                cur0 /= 2;
            } else if (j==10) {
                if (cur0%2==0)
                    ss = s2;
                else
                    ss = s3;
                memcpy(buffer+59, ss, 5);
                cur0 /= 2;
            } else {
                if (cur0%3==0)
                    ss = s0;
                else if (cur0%3==1)
                    ss = s1;
                else
                    ss = s4;
                memcpy(buffer+j*6-1, ss, 6);
                cur0 /= 3;
            }
        }
    }
}

void cons1(long cur0, int which, long ii) {
    for (int j=0; j<C; j++) {
        if (cur0%2==0)
            switch(which) {
                case 1: memcpy(buffer+sz*j, buf00[ii*C+j], sz1);break;
                case 2: memcpy(buffer+sz*j, buf10[ii*C+j], sz1);break;
                case 3: memcpy(buffer+sz*j, buf20[ii*C+j], sz1);break;
                default: assert(0);
            }
        else
            switch(which) {
                case 1: memcpy(buffer+sz*j, buf01[ii*C+j], sz1);break;
                case 2: memcpy(buffer+sz*j, buf11[ii*C+j], sz1);break;
                case 3: memcpy(buffer+sz*j, buf21[ii*C+j], sz1);break;
                default: assert(0);
            }
        cur0 /= 2;
    }
}

int main() {
    srand(time(NULL));
    long ii,i,j,cur,cur0;
    uint32_t state,data;
    int which=0;
    state = 0x67452301;
    for (ii=0; ii<C*C*C; ii++) {
    d.clear();
    while (true) {
        cur = rand()%314928;
        cons0(cur);
        data = hash_block((uint32_t*)(buffer), state, which);
        it = d.find(data);
        if (it!=d.end()&&it->second!=cur) {
            memcpy(buf00[ii], buffer, 64);
            cons0(it->second);
            memcpy(buf01[ii], buffer, 64);
            state = data;
            break;
        }
        d[data] = cur;
    }
    printf("buf0: %ld\n",ii);
    }
    /*
    printf("%s\n", buf00[0]);
    printf("%s\n", buf01[0]);
    uint32_t data1,data0;
    data0 = starting_state(0);
    data1 = starting_state(0);
    for (i=0;i<C;i++) {
    data0 = hash_block((uint32_t*)(buf00[i]), data0, 0);
    printf("%08x\n", data0);
    data1 = hash_block((uint32_t*)(buf01[i]), data1, 0);
    printf("%08x\n", data1);
    }
    return 0;
    */

    for (i=1; i<4; i++) {
        int sii;
        state = starting_state(i);
        switch(i) {
            case 1: sii=C*C;sz=64;break;
            case 2: sii=C;sz=64*C;break;
            case 3: sii=1;sz=64*C*C;break;
            default: assert(0);
        }
        sz1 = sz*C;
        for (ii=0; ii<sii; ii++) {
        printf("buf%ld %ld\n", i, ii);
        d.clear();
        while (true) {
            cur = rand()%131072;
            cons1(cur,i,ii);
            data = state;
            for (j=0; j<sz1; j+=64)
                data = hash_block((uint32_t*)(buffer+j), data, i);
            it = d.find(data);
            if (it!=d.end()&&it->second!=cur) {
                switch(i) {
                    case 1: memcpy(buf10[ii], buffer, sz1);break;
                    case 2: memcpy(buf20[ii], buffer, sz1);break;
                    case 3: memcpy(buf30[ii], buffer, sz1);break;
                    default: assert(0);
                }
                cons1(it->second, i, ii);
                switch(i) {
                    case 1: memcpy(buf11[ii], buffer, sz1);break;
                    case 2: memcpy(buf21[ii], buffer, sz1);break;
                    case 3: memcpy(buf31[ii], buffer, sz1);break;
                    default: assert(0);
                }
                state = data;
                break;
            }
            d[data] = cur;
        }
        /*
        if (i==1) {
    printf("%s\n", buf10[0]);
    printf("%s\n", buf11[0]);
            data=starting_state(0);
            for (j=0; j<sz1; j+=64)
                data = hash_block((uint32_t*)(buf10[0]+j), data, 0);
            printf("%08x\n", data);
            data=starting_state(1);
            for (j=0; j<sz1; j+=64)
                data = hash_block((uint32_t*)(buf10[0]+j), data, 1);
            printf("%08x\n", data);
            data=starting_state(0);
            for (j=0; j<sz1; j+=64)
                data = hash_block((uint32_t*)(buf11[0]+j), data, 0);
            printf("%08x\n", data);
            data=starting_state(1);
            for (j=0; j<sz1; j+=64)
                data = hash_block((uint32_t*)(buf11[0]+j), data, 1);
            printf("%08x\n", data);
        }
        if (i==2) {
    printf("%s\n", buf20[0]);
    printf("%s\n", buf21[0]);
            data=starting_state(0);
            for (j=0; j<sz1; j+=64)
                data = hash_block((uint32_t*)(buf20[0]+j), data, 0);
            printf("%08x\n", data);
            data=starting_state(1);
            for (j=0; j<sz1; j+=64)
                data = hash_block((uint32_t*)(buf20[0]+j), data, 1);
            printf("%08x\n", data);
            data=starting_state(2);
            for (j=0; j<sz1; j+=64)
                data = hash_block((uint32_t*)(buf20[0]+j), data, 2);
            printf("%08x\n", data);
            data=starting_state(0);
            for (j=0; j<sz1; j+=64)
                data = hash_block((uint32_t*)(buf21[0]+j), data, 0);
            printf("%08x\n", data);
            data=starting_state(1);
            for (j=0; j<sz1; j+=64)
                data = hash_block((uint32_t*)(buf21[0]+j), data, 1);
            printf("%08x\n", data);
            data=starting_state(2);
            for (j=0; j<sz1; j+=64)
                data = hash_block((uint32_t*)(buf21[0]+j), data, 2);
            printf("%08x\n", data);
        }
        if (i==3) {
            memcpy(buf30+sz*17, "apple", 5);
            memcpy(buf31+sz*17, "apple", 5);
            printf("----\n");
            data = hash_block((uint32_t*)(buf30), state, 0);
            printf("%08x\n", data);
            data = hash_block((uint32_t*)(buf30), state, 1);
            printf("%08x\n", data);
            data = hash_block((uint32_t*)(buf30), state, 2);
            printf("%08x\n", data);
            data = hash_block((uint32_t*)(buf30), state, 3);
            printf("%08x\n", data);
            data = hash_block((uint32_t*)(buf31), state, 0);
            printf("%08x\n", data);
            data = hash_block((uint32_t*)(buf31), state, 1);
            printf("%08x\n", data);
            data = hash_block((uint32_t*)(buf31), state, 2);
            printf("%08x\n", data);
            data = hash_block((uint32_t*)(buf31), state, 3);
            printf("%08x\n", data);
        }
        */
        
    }
    }
    printf("%s\n", buf30[0]);
    printf("%s\n", buf31[0]);
    return 0;

}
