from pwn import *
import sys

context.log_level='error'

def tostr(x):
    a=hex(x)[2:]
    if a[-1]=='L':
        a=a[:-1]
    if len(a)%2==1:
        a='0'+a
    return a.decode('hex')

def once(ct):
    assert len(ct)==128
    c = remote('perfect-secrecy.ctfcompetition.com', 1337)
    c.send('0')
    c.send('1')
    c.send(ct)
    res = c.recv()
    c.close()
    if res[0]=='\x00':
        return 0
    else:
        return 1

def lsb(ct):
    test=tostr(ct)
    test=test.rjust(128,'\x00')
    stat = [0,0]
    for i in range(20):
        a = once(test)
        stat[a]+=1
    while abs(stat[0]-stat[1])<7:
        a = once(test)
        stat[a]+=1
    print stat
    if stat[0]>stat[1]:
        return 0
    else:
        return 1

with open('flag.txt','rb') as f:
    ct=f.read()
ct=int(ct.encode('hex'),16)
n=153314286737753283255547252902231988923677001570537670823569737192417931917849858323550190365704182153062786056662711312188848241990605760007378096173801480759292810572306932509446953082431394351272757346605609898944553806892979792999103404028562806843687533668219905113924888506316958727392199113512716600273
e=65537
low=0
high=n
bits=[-1]*1024
ll=int(sys.argv[1])
rr=int(sys.argv[2])
for i in range(1024):
    ct = ct*pow(2,e,n)%n
    if i>=ll and i<rr:
        print i
        bit = lsb(ct)
        bits[i]=bit
print bits[ll:rr]
