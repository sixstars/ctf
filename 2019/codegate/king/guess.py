#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *
elf = ELF("./KingMaker")
data = elf.read(0x4011BB,7)
for i in range(0x10,0xf0,0x10):
    code = "UH\x89\xe5H\x83\xec"#+chr(i)+"dH"
    flag =  "".join([chr(ord(x)^ord(y)) for x,y in zip(code,data)])
    print flag.encode("hex"),flag



