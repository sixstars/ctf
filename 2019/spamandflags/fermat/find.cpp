#include <stdio.h>
#include <stdlib.h>
#include<map>

using namespace std;

long long safe_add(long long x, long long y)
{
    long long r = x + y;
    if (r < x)
        return -1;
    return r;
}

long long safe_mul(long long x, long long y)
{
    long long r = x * y;
    if (r < x)
        return -1;
    return r;
}

long long safe_pow(long long x, long long n)
{
    long long r0 = 1, r1 = x;
    for (int i = 63; i >= 0; i--) {
        if (n & (1LL << i)) {
            r0 = safe_mul(r0, r1);
            r1 = safe_mul(r1, r1);
        } else {
            r1 = safe_mul(r0, r1);
            r0 = safe_mul(r0, r0);
        }
        if (r0==-1||r1==-1)
            return -1;
    }
    return r0;
}

map<long long, long long> d;
map<long long, long long>::iterator it0,it1;


int main(void)
{  
    srand(time(NULL));
    long long a3, b3, c, c3;
    long i;
    d.empty();
    long cnt = 0;
    while (true) {
        c = rand();
        c = c<<32;
        c += rand();
        c3 = safe_pow(c,3);
        if (c3==-1)
            continue;
        d[c3] = c;
        cnt++;
        if (cnt%1000000==0)
            printf("1. cnt:%ld\n", cnt);
        if (cnt>(1<<27))
            break;
    }
    cnt = 0;
    while (true) {
        c = rand();
        c = c<<32;
        c += rand();
        c3 = safe_pow(c,3);
        if (c3==-1)
            continue;
        if (cnt%10==0)
            printf("2. cnt: %ld\n", cnt);
        cnt++;
        for (it0=d.begin();it0!=d.end(); it0++) {
            it1 = d.find(c3-it0->first);
            if (it1!=d.end()) {
                printf("found\n");
                printf("%lld, %lld, %lld\n", it0->second, it1->second, c);
            }
        }
    }
    return 0;
}
