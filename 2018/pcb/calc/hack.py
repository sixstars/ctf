#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./easycalc"
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

def create(idx,size,a,con,b=0):
    r.sendlineafter("input>\n","1")
    r.sendlineafter("index\n",str(idx))
    r.sendlineafter("size",str(size))
    r.sendline("%d %d"%(a,b))
    r.sendafter("string\n",con)

def edit(idx,a,b):
    r.sendlineafter("input\n","3")
    r.sendlineafter("index\n",str(idx))
    r.sendlineafter("a and b\n","%d %d"%(a,b))

def drop(idx):
    r.sendlineafter("input\n","4")
    r.sendlineafter("index\n",str(idx))

create(0,0x200,1,"a")
create(1,0x200,1,"a")


r.interactive()











