由于unpad部分并未检查最后一位的范围，所以可以让它减去超过一个block的大小，所以先让服务器签一个`admin`开头的用户名，再找一个拼接后末尾为`0x1b`的密文块，利用CBC特性我们可以xor算出新构造的密文解密后的结果，就能得到其md5值，IV完全可控所以第一个块的内容可以由我们任意设置，确保过掉md5的检查。

代码如下
```
from hashlib import md5
from pwn import *

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[0:-ord(s[-1])]

def str2num(s):
    return int(s.encode('hex'),16)

def num2str(n):
    return hex(n)[2:].rjust(32,'0').decode('hex')

context.log_level='debug'

name1='admin1'
m1=md5(pad(name1)).digest()

c = remote('202.120.7.217',8221)
c.recvline()
c.recvline()
c.sendline('r')
c.sendline(name1)
c.recvline()
t=c.recvline()
print t
iv1=t[:32].decode('hex')
c11=t[32:64].decode('hex')
c12=t[64:96].decode('hex')
i=0
while True:
    i+=1
    c.recvline()
    c.sendline('r')
    c.sendline(str(i))
    c.recvline()
    c2=c.recvline()
    name2=pad(str(i))
    c21=t[32:64].decode('hex')
    if ord(name2[-1])^int(c2[62:64],16)^ord(c12[-1])==0x1b:
        print i
        break


iv2=c2[:32].decode('hex')
c21=c2[32:64].decode('hex')
c22=c2[64:96].decode('hex')

pay2=''
for i in range(16):
    pay2+=chr(ord(name2[i])^ord(c21[i])^ord(c12[i]))

m3=md5(pad(name1)+pay2).digest()

iv3=''
for i in range(16):
    iv3+=chr(ord(iv1[i])^ord(m1[i])^ord(m3[i]))
payload=iv3+c11+c12+c22
c.recvline()
c.sendline('l')
c.sendline(payload.encode('hex'))
c.recv()
c.interactive()
```
