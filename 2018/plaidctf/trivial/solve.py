import binascii
import collections
import hashlib
import random
import os
import string
import sys
from itertools import product
from hashlib import sha256
from pwn import *
from subprocess import check_output


def bytestobits(b):
    return [(ord(byte) >> (7-i)) & 1 for byte in b for i in range(8)]

def bitstobytes(b):
    return ''.join(map(chr,([sum(b[i+j] << (7-j) for j in range(8)) for i in range(0, len(b), 8)])))

def trivium(key, iv, numbytes):
    assert(len(key) == 10)
    assert(len(iv) == 10)

    init_list = bytestobits(key)
    init_list += [0]*13

    init_list += bytestobits(iv)
    init_list += [0]*4

    init_list += [0]*108
    init_list += [1, 1, 1]
    state = collections.deque(init_list)

    def genbit():
        t_1 = state[65]  ^ state[92]
        t_2 = state[161] ^ state[176]
        t_3 = state[242] ^ state[287]

        out = t_1 ^ t_2 ^ t_3

        s_1 = t_1 ^ state[90]  & state[91]  ^ state[170]
        s_2 = t_2 ^ state[174] & state[175] ^ state[263]
        s_3 = t_3 ^ state[285] & state[286] ^ state[68]
        #print(t_3,s_3)

        state.rotate(1)

        state[0] = s_3
        state[93] = s_1
        state[177] = s_2

        return out
    def genbit2():
        global cur
        m=288
        t_1 = state[(cur+65)%m]  ^ state[(cur+92)%m]
        t_2 = state[(cur+161)%m] ^ state[(cur+176)%m]
        t_3 = state[(cur+242)%m] ^ state[(cur+287)%m]

        out = t_1 ^ t_2 ^ t_3

        s_1 = t_1 ^ state[(cur+90)%m]  & state[(cur+91)%m]  ^ state[(cur+170)%m]
        s_2 = t_2 ^ state[(cur+174)%m] & state[(cur+175)%m] ^ state[(cur+263)%m]
        s_3 = t_3 ^ state[(cur+285)%m] & state[(cur+286)%m] ^ state[(cur+68)%m]
        #print(cur,t_3,s_3)

        state[(cur+287)%m] = s_3
        state[(cur+92)%m] = s_1
        state[(cur+176)%m] = s_2

        cur -= 1

        return out

    # warmup
    for i in range(576):
        genbit()

    # generate keystream
    stream = [genbit() for i in range(8*numbytes)]

    return stream


def pwnbak(keypos, outpos, ivpos):
    key=[0]*80
    key=bitstobytes(key)
    key=os.urandom(10)
    #iv=os.urandom(10)
    total = 0
    for it in product(range(2),repeat=len(ivpos)):
        iv=[0]*80
        for i in range(len(ivpos)):
            iv[ivpos[i]-1] = it[i]
        iv=bitstobytes(iv)
        sth=trivium(key,iv,16)
        a=sth[outpos-577]
        total ^= a
    
    total2 = 0
    kbits = bytestobits(key)
    for kp in keypos:
        total2 ^= kbits[kp-1]
    return total, total2

def pwn(outpos, ivpos):
    total = 0
    for it in product(range(2),repeat=len(ivpos)):
        iv=[0]*80
        for i in range(len(ivpos)):
            iv[ivpos[i]-1] = it[i]
        iv=bitstobytes(iv).encode('hex')
        assert len(iv)==20
        numb = min(16, (outpos-577)/8+1)
        c.sendline('keystream %s %d' % (iv, numb))
        res = c.recvline().strip().decode('hex')
        a=bytestobits(res)[outpos-577]
        total ^= a
    return total
    

stat = [ [1, 597, [ 4, 7, 12, 15, 2, 56 ]],
[4, 579, [ 4, 7, 12, 15, 6, 47 ]],
[5, 577, [ 7, 12, 15, 1, 79 ]],
[6, 611, [ 4, 7, 12, 15, 41, 51 ]],
[8, 589, [ 4, 7, 12, 15, 23, 54 ]],
[9 ,589, [ 4, 7, 12, 15, 36, 63 ]],
[11, 595, [ 4, 7, 12, 15, 24, 41 ]],
[14, 604, [ 4, 7, 12, 15, 21, 32 ]],
[16, 578, [ 4, 7, 12, 15, 77, 79 ]],
[17, 588, [ 4, 7, 12, 15, 20, 79 ]],
[19, 587, [ 4, 7, 12, 15, 23, 40 ]],
[25, 580, [ 4, 12, 15, 23, 49 ]],
[26, 580, [ 4, 12, 15, 22, 49 ]],
[27, 579, [ 4, 7, 12, 23, 48 ]],
[36, 583, [ 4, 7, 12, 34, 44 ]],
[38, 580, [ 7, 12, 15, 49, 55 ]],
[39, 578, [ 7, 12, 15, 52, 79 ]],
[55, 598, [ 4, 7, 12, 15, 51, 58 ]],
[56, 578, [ 4, 7, 12, 15, 26, 50 ]],
[61, 587, [ 4, 7, 12, 15, 40, 74 ]],
[62, 604, [ 4, 7, 12, 15, 23, 75 ]],
[63, 604, [ 4, 7, 12, 15, 23, 74 ]],
[64, 597, [ 4, 7, 12, 15, 3, 30 ]],
[65, 580, [ 4, 7, 12, 15, 2, 33 ]],
[66, 580, [ 4, 7, 12, 15, 16, 34 ]],
[67, 596, [ 4, 7, 12, 15, 40, 65 ]],
[68, 596, [ 4, 7, 12, 15, 40, 64 ]],
[15, 581, [ 4, 28, 31, 79, 3, 47 ]],
[18, 600, [ 4, 28, 31, 79, 1, 69 ]],
[20, 598, [ 4, 28, 31, 79, 3, 50 ]],
[23, 625, [ 4, 28, 31, 79, 8, 12 ]],
[30, 606, [ 4, 28, 31, 79, 12, 46 ]],
[32, 606, [ 4, 28, 31, 79, 1, 17 ]],
[33, 591, [ 28, 31, 79, 2, 37 ]],
[35, 589, [ 4, 28, 31, 79, 14, 51 ]],
[58, 588, [ 4, 28, 31, 79, 35, 38 ]],
[21, 583, [ 2, 7, 8, 12, 19, 45 ]],
[22, 583, [ 2, 7, 8, 12, 20, 56 ]],
#[10, 583, [ 2, 8, 12, 80, 19, 43 ]],
#[12, 582, [ 2, 8, 12, 80, 19, 44 ]],
[58, 607, [ 2, 8, 12, 80, 19, 71 ]],
[7, 598, [3, 11, 13, 1, 7, 53]],
[12, 581, [3, 11, 13, 1, 23, 25]],
[13, 585, [3, 11, 13, 1, 9, 51]],
[28, 589, [3, 11, 13, 1, 19, 41]],
[34, 583, [3, 11, 13, 1, 7, 47]],
[37, 582, [3, 11, 13, 1, 9, 48]],
[40, 582, [3, 11, 13, 1, 9, 38]],
[41, 582, [3, 11, 13, 1, 9, 37]],
[31, 586, [5, 7, 9, 1, 29, 37]],
[49, 604, [5, 7, 9, 1, 45, 75]],
[50, 589, [5, 7, 9, 2, 48, 51]],
[51, 589, [5, 7, 9, 2, 36, 47]],
[53, 585, [5, 7, 9, 1, 40, 51]],
[54, 585, [5, 7, 9, 1, 40, 50]],
[10, 588, [5, 8, 11, 1, 14, 49]],
[24, 582, [5, 8, 11, 1, 20, 54]],
[47, 600, [5, 8, 11, 1, 36, 45]],
[48, 600, [5, 8, 11, 1, 36, 44]],
#
[69, 579, [ 2, 8, 12, 80, 14, 49 ]]]
stat2 = [[2 , 65, 580, [ 4, 7, 12, 15, 8, 33 ]],
[3 , 66, 580, [ 4, 7, 12, 15, 14, 32 ]],
[57 , 63, 588, [ 4, 7, 12, 14, 24 ]],
[59 , 65, 612, [ 4, 7, 12, 15, 10, 41 ]],
[60 , 66, 589, [ 4, 12, 15, 38, 48 ]]]
'''
print len(stat2)+len(stat)
for i in [25,26,35,38,39]:#range(len(stat)):
    cnt1=0
    cnt2=0
    for j in range(30):
        d0,d1 = pwnbak([stat[i][0]], stat[i][1], stat[i][2])
        if d0==d1:
            cnt1+=1
        else:
            cnt2+=1
        if cnt1>0 and cnt2>0:
            print i
            print 'gya!'
            break
    print cnt1,cnt2
for i in [1]:#range(len(stat2)):
    for j in range(30):
        d0,d1 = pwnbak([stat2[i][0],stat2[i][1]], stat2[i][2], stat2[i][3])
        if d0==d1:
            print i
            print 'gya!'
            break
exit()
'''
def dopow():
    tab=string.ascii_letters+string.digits
    c.recvuntil('with ')
    pre=c.recv(10)
    print pre
    i=0
    while True:
        cur=random.sample(tab,6)
        if sha256(pre+cur).hexdigest()[-6:] == ('ffffff'):
            return pre+cur
        i+=1


c = remote('trivial.chal.pwning.xxx',5419)

work = dopow()
print work
c.sendline(work)
c.recvuntil('[key]\n')
kbits = [-1]*80
for i in range(len(stat)):
    k = pwn(stat[i][1], stat[i][2])
    if i in [25,26]:
        kbits[stat[i][0]-1] = 1 ^ k
    else:
        if kbits[stat[i][0]-1]!=-1:
            print stat[i]
        kbits[stat[i][0]-1] = k
for i in range(len(stat2)):
    k = pwn(stat2[i][2], stat2[i][3])
    if i==1:
        kbits[stat2[i][0]-1] = 1 ^ k ^ kbits[stat2[i][1]-1]
    else:
        kbits[stat2[i][0]-1] = k ^ kbits[stat2[i][1]-1]
c.sendline('keystream '+'00'*10+' 16')
res = c.recvline().strip().decode('hex')
res = bytestobits(res)
print kbits
f = open('stats','w')
for i in range(80):
    f.write('%d ' % kbits[i])
f.write('\n')
for i in range(128):
    f.write('%d ' % res[i])
f.close()
t=check_output('./a.out')
t=eval('['+t+']')
key=bitstobytes(t).encode('hex')
context.log_level='debug'
c.sendline('guess '+key)
c.recv()
c.recv()
c.interactive()
    
