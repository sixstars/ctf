#include<iostream>
#include<fstream>
#include<stdint.h>

using namespace std;

uint8_t genone(uint8_t *state, int cur) {
    const int m=288;
    uint8_t t1 = state[(cur+65)%m]  ^ state[(cur+92)%m];
    uint8_t t2 = state[(cur+161)%m] ^ state[(cur+176)%m];
    uint8_t t3 = state[(cur+242)%m] ^ state[(cur+287)%m];
    uint8_t out = t1^t2^t3;

    uint8_t s1 = t1 ^ state[(cur+90)%m]  & state[(cur+91)%m]  ^ state[(cur+170)%m];
    uint8_t s2 = t2 ^ state[(cur+174)%m] & state[(cur+175)%m] ^ state[(cur+263)%m];
    uint8_t s3 = t3 ^ state[(cur+285)%m] & state[(cur+286)%m] ^ state[(cur+68)%m];

    state[(cur+287)%m] = s3;
    state[(cur+92)%m] = s1;
    state[(cur+176)%m] = s2;
    return out;
}
uint8_t state[288];
uint8_t res[256];

void trivium(uint8_t key[80], uint8_t iv[80], int numbits) {
    int i;
    for (i=0;i<80;i++)
        state[i] = key[i];
    for (i=80;i<93;i++)
        state[i] = 0;
    for (i=93;i<173;i++)
        state[i] = iv[i-93];
    for (i=173;i<285;i++)
        state[i] = 0;
    for (i=285;i<288;i++)
        state[i] = 1;
    int cur = 288*10;
    for (i=0;i<576;i++) {
        genone(state, cur);
        /*
        for (int j=0;j<288;j++)
            cout<<int(state[j])<<' ';
        cout<<endl;
        */
        cur--;
    }
    for (i=0;i<numbits;i++) {
        res[i] = genone(state, cur);
        cur--;
    }
    return;
}
uint8_t key[80], iv[80];
int tar[128];
int bpos[35];
long po2[35];

int main() {
    int i,bi;
    int a;
    ifstream fin("stats");
    bi=0;
    for (i=0;i<80;i++) {
        fin>>a;
        if (a==-1) {
            bpos[bi] = i;
            bi++;
        } else {
            key[i]=a;
        }
    }
    for (i=0;i<128;i++) 
        fin>>tar[i];
    for (i=0;i<80;i++)
        iv[i]=0;
    po2[0]=1;
    for (i=1;i<35;i++)
        po2[i]=po2[i-1]<<1;
    for (long ii=0; ii<po2[18]; ii++) {
        for (i=0;i<18;i++)
            if ((ii&po2[i])>0) {
                key[bpos[i]]=1;
            }else{
                key[bpos[i]]=0;
            }
        trivium(key,iv,128);
        bool ok = true;
        for (i=0;i<128;i++)
            if (int(res[i]) != tar[i])
                ok=false;
        if (ok) {
            for (i=0;i<80;i++)
                cout<<int(key[i])<<',';
            break;
        }
    }
    return 0;
}
