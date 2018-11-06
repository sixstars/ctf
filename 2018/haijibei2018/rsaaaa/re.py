#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *
from pwnlib.util.iters import bruteforce
import hashlib
context.log_level="debug"

def hash(x):
    return hashlib.sha512(x).hexdigest()

r=remote("106.75.101.197",7544)
r.recvuntil("sha512(")
prefix=r.recvuntil("+")[:-1]
r.recvuntil("== ")
result=r.recvline()[:-1]
x=bruteforce(lambda x:hash(prefix+x)==result,string.ascii_letters+string.digits,length=4,method='downfrom')
r.sendline(x)
r.recvuntil("age:")
msg1=int(r.recvline()[:-1],16)
m=msg1
r.recvuntil("text:")
c=int(r.recvline()[:-1],16)
r.sendlineafter("n:",str(c-m))
r.sendlineafter("d:","1")
r.recvuntil("n=")

n=int(r.recvline(),16)
r.recvuntil("e=")
e=int(r.recvline(),16)
r.recvuntil("c=")
c=int(r.recvline(),16)

import gmpy2
x=gmpy2.invert(c,n)
r.sendline(str(x))
r.recvuntil("message:")
msg=int(r.recvline(),16)
msg2=gmpy2.invert(msg,n)
r.sendline(str(msg2))
r.recvuntil("flag:")
flag=r.recvline()[:-1][2:].decode("hex")

from Crypto.Cipher import AES
cipher = AES.new(hex(msg2)[2:].decode("hex"), AES.MODE_CBC, hex(msg1)[2:].decode("hex"))
print cipher.decrypt(flag)

r.interactive()
