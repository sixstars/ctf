#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *
elf=ELF("./payload_x86.elf")

const=map(ord,elf.read(0x6CD100,0x20))
mixer=elf.read(0x6CD120,0x200)
input=[0]*256

set=[]
for i in range(0,0x100):
    v=u16(mixer[i*2:i*2+2])
    p=v&1
    idx=v>>1
    print hex(v),hex(idx),p
    bit=(const[i>>3]>>(i&7))&1
    print bit
    if p==1:
        bit^=1
    input[idx]=bit

key=[]
for i in range(0,256,8):
    x=int("".join(map(str,input[i:i+8][::-1])),2)
    key.append(chr(x))

key= "".join(key)
print key.encode("hex")
with open("x86_key","w+") as f:
    f.write(key)



