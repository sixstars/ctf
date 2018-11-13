#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *
elf=ELF("./payload_ppc.elf")
mixer=map(ord,elf.read(0x100B0008,0x20))
result="25f98f003866ed1f229b3e24a55e58ca"

key=[' ']*32

for i in range(0,32):
    p=result[i]
    idx=mixer[i]
    key[idx]=p

key= "".join(key)
print key
with open("arm_key","w+") as f:
    f.write(key)



