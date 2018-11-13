#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *
import gmpy2
elf=ELF("./payload_arm.elf")

def hash(a1):
    return (0x3E37D15F * a1 - 0x3B07D9B9) % 0x7917ED55

def dehash(i):
    return ((((0x3E37D15F * i)&0xffffffff)- 0x3B07D9B9) &0xffffffff)% 0x7917ED55

const=elf.read(0x079088,0x20*4)

ret=[]
for i in range(0,32):
    v=u32(const[i*4:i*4+4])
    pt=dehash(v)
    


exit(0)
key=[]
for i in range(0,256,8):
    x=int("".join(map(str,input[i:i+8][::-1])),2)
    key.append(chr(x))

key= "".join(key)
print key.encode("hex")
with open("x86_key","w+") as f:
    f.write(key)



