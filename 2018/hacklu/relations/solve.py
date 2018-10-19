from Crypto.Cipher import AES
import base64
from pwn import *

#context.log_level='debug'

stats = []
for i in range(256):
    tmp = []
    for ji in range(8):
        j = 2**ji
        if (i+j)==(i^j):
            tmp.append(1)
        else:
            tmp.append(0)
    stats.append(tmp)

c = remote('arcade.fluxfingers.net', 1821)

def dodec(k):
    c.sendlineafter('----*', 'DEC')
    c.sendlineafter('>>> ', k)
    c.recvuntil(' is  ')
    res = c.recv(0x40)
    assert len(res)%16==0
    return res

def doadd(op):
    c.sendlineafter('----*', 'ADD')
    c.sendlineafter('>>> ', op)
    c.recvuntil(' is  ')
    res = c.recvuntil('==\n').replace('\n','')
    return res.decode('base64')

def doxor(op):
    c.sendlineafter('----*', 'XOR')
    c.sendlineafter('>>> ', op)
    c.recvuntil(' is  ')
    res = c.recvuntil('==\n').replace('\n','')
    return res.decode('base64')

k = '\x00'*16
ct = dodec(base64.b64encode(k))
a = AES.new(k)
pt = a.encrypt(ct)
print pt.encode('hex')
'''
k = '1'*16
ct = dodec(base64.b64encode(k))
a = AES.new(k)
pt = a.encrypt(ct)
print pt.encode('hex')
'''

ans = ''
for i in range(0x10):
    cur = [0]*(i+1)
    tmp = []
    for j in range(8):
        print i,j
        cur[0] = 2**j
        v = ''.join(map(chr,cur))
        a1 = doadd(v.encode('hex'))
        a2 = doxor(v.encode('hex'))
        if a1==a2:
            tmp.append(1)
        else:
            tmp.append(0)
    print tmp
    for j in range(256):
        if tmp == stats[j]:
            ans = chr(j) + ans
            print ans.encode('hex')
            break

print pt.encode('hex')

c.interactive()
