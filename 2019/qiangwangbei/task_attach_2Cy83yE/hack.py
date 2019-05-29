#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./trywrite"
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
def add(key,data):
    r.sendlineafter(">>","1")
    r.sendlineafter("key:",key)
    r.sendafter("data",data)

def show(idx):
    r.sendlineafter(">>","2")
    r.sendlineafter("index:\n",str(idx))
    return r.recvline()
def del(idx):
    r.sendlineafter(">>","3")
    r.sendlineafter("index:\n",str(idx))

def changeMsg()
r.sendlineafter("heap:","0")


r.interactive()
