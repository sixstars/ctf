#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *
context.log_level="error"
module="CTF{7517f720e28c4aceb18eb1563ef0%s}"

def save_flag(x):
    with open("./flag","w+") as fa:
        fa.write("".join(x))

def br(flag):
    flag+="\x00"*0x40
    save_flag(flag)
    r=process(("./f -m flag.mgc flag").split(" "))
    p=r.recvuntil("ERROR: name use count (30) exceeded")
    r.close()
    print flag[:-0x40],len(p)
    return len(p)

first=br(module%'0000')
for i in range(0xf03f,0,-1):
    flag=module%('%04x'%i)
    if first != br(flag):
        break
