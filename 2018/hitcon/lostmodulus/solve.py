from hashlib import sha1
import itertools
import math
import string
from pwn import *

#context.log_level='debug'
def tostr(x):
    tmp = hex(x)[2:].strip('L')
    if len(tmp)%2==1:
        tmp = '0'+tmp
    return tmp.decode('hex')

def enc(x):
    c.sendlineafter('cmd: ','A')
    c.sendlineafter('input: ',tostr(x).encode('hex'))
    res = int(c.recvline(),16)
    return res

def once(x):
    c.sendlineafter('cmd: ','B')
    c.sendlineafter('input: ',tostr(x).encode('hex'))
    res = int(c.recvline(),16)
    return res

def cons(x):
    res = 1
    for i in range(1024):
        if x%2==1:
            res *= cts[i]
        x /= 2
    return res 


c = remote('13.112.92.9', 21701)
#c = process('./crypto.py')


'''
#oracle
n = int(c.recvline())
'''

c.recvline()
cf = int(c.recvline(),16)
print hex(cf)
cts = []
for i in range(1024):
    if i%4==0:
        tmp = enc(2**i)
        cts.append(tmp)
    else:
        cts.append(cts[i-1]**2)
upper = 2**1024
lower = 0
base = 0
ctbase = 1
for i in range(1024):
    print 'round',i
    mid = (upper+lower)/2
    if i%6==1:
        base = lower
        ctbase = enc(base)
    cur = ctbase * cons(mid-base)
    if once(cur**2)%2==0:
        upper = mid
    else: 
        lower = mid

'''
print n
print upper
print lower
'''
n=upper
length = 1024
upper = n
lower = 0
cur = cf
pre = '0'*448
stats=''
for i in range(length):
    print 'round',i,stats

    cur = pow(cur,2,n**2)
    if len(pre)>i:
        res = int(pre[i])
    else:
        res = once(cur)%2
    if res==0:
        stats += '0'
        upper = (upper + lower)/2
    else: 
        stats += '1'
        lower = (upper + lower)/2
    if upper < lower:
        break

print '\nFlag:'
print hex(int(upper))[2:].strip('L')
print hex(int(lower))[2:].strip('L')

c.interactive()
exit()
