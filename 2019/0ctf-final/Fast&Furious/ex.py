#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
from pwn import *
elf=ELF("./linux")
print "rdi"
for i in range(-0x100,0x100,8):
    for p in elf.search(asm("jmp [rdi+%d]"%i,arch="amd64")):
        print "jmp [rdi+0x%x]"%i,hex(p)


for i in range(-0x100,0x100,8):
    for p in elf.search(asm("jmp [rbx+%d]"%i,arch="amd64")):
        print "jmp [rbx+0x%x]"%i,hex(p)

for i in range(-0x100,0x100,8):
    for p in elf.search(asm("jmp [r14+%d]"%i,arch="amd64")):
        print "jmp [r14+0x%x]"%i,hex(p)
for i in range(-0x100,0x100,8):
    for p in elf.search(asm("jmp [r15+%d]"%i,arch="amd64")):
        print "jmp [r15+0x%x]"%i,hex(p)
