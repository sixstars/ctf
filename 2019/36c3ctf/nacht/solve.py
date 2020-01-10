from pwn import *
import ctypes
from Crypto.Util.number import *
from itertools import product
context.log_level='debug'

lib = ctypes.CDLL('./tweetnacl.so')

p130 = 2**130-5
p128 = 2**128

def mac(key, msg):
    tag = ctypes.create_string_buffer(16)
    lib.crypto_onetimeauth_poly1305_tweet(tag, key, len(msg), msg)
    return tag.raw

def toint(s):
    return int(s[::-1].encode('hex'),16)

def fromint(x):
    tmp = long_to_bytes(x)[::-1]
    return tmp.ljust(16,'\x00')

def trycalc1(m,k):
    c1 = toint(k[:16]+'\x01')
    c2 = toint(k[16:]+'\x01')
    r = toint(m[:16])
    r &= 0xff0ffffffc0ffffffc0ffffffc0fffffff
    s = toint(m[16:])
    res = ((c1*r**2+c2*r)%p130+s)%p128
    return res

def trycalc(m,c1,c2):
    r = toint(m[:16])
    r &= 0xff0ffffffc0ffffffc0ffffffc0fffffff
    s = toint(m[16:])
    res = ((c1*r**2+c2*r)%p130+s)%p128
    return res

def getmid(m,t):
    s = toint(m[16:])
    return (toint(t)-s)%p128

'''
k = '\x01'+'\x00'*15+'\x00'+'\x00'*15
#k = 'a\xca5\x84\xae\xa6g\xbc:q"\x8a\x13\xd4E%\x1e\xb6J\xfe\xfe\xc9\x9a\xb9i\xd2!\xe9\xb1\xa0\x8aI'
m0 = '\x06'+'\x01'*15+'\x00'*16
m1 = '\x06'+'\x00'*15+'\x00'*16
m = '\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01\x01'
m2 = m
t0 = fromint(trycalc1(m0,k))
t1 = fromint(trycalc1(m1,k))
t2 = fromint(trycalc1(m2,k))
t = mac(k,m)
print toint(t)
t2 = trycalc1(m,k)
print t2

exit()
'''

c = remote('88.198.156.141', 2833)
#c = process('./vuln.py')

ms = []
ts = []
for i in range(32):
    a,b = c.recvline().strip().split(' ')
    ms.append(a.decode('hex'))
    ts.append(b.decode('hex'))

r0 = toint(ms[0][:16])&0xff0ffffffc0ffffffc0ffffffc0fffffff
r02 = pow(r0,2)
r1 = toint(ms[1][:16])&0xff0ffffffc0ffffffc0ffffffc0fffffff
r12 = pow(r1,2)
tmp0 = getmid(ms[0],ts[0])
tmp1 = getmid(ms[1],ts[1])

found = False
for i,j in product(range(4),repeat=2):
    mid0 = tmp0+p128*i
    mid1 = tmp1+p128*j
    res0 = (mid0*r12-mid1*r02)%p130
    res1 = inverse((r0*r12-r1*r02)%p130,p130)
    c2 = res0*res1%p130
    c1 = (mid0-c2*r0)%p130*inverse(r02,p130)%p130
    if trycalc(ms[2],c1,c2) == toint(ts[2]):
        print 'found'
        print c1,c2
        found = True
        break

if not found:
    print ':('
    exit()

for i in range(32):
    assert trycalc(ms[i],c1,c2) == toint(ts[i])

m,_ = c.recvline().strip().split(' ')

m = m.decode('hex')
ans = fromint(trycalc(m, c1, c2))
c.sendline(ans.encode('hex'))
c.interactive()
