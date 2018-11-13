#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *
elf=ELF("./payload_s390.elf")
const=elf.read(0x10980d8,0x20*4)

for i in range(0x20):
    v=u32(const[i*4:i*4+4],endian="big")
    print chr((v-37)/13),
