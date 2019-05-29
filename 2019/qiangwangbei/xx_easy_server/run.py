#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
from pwn import *
elf = ELF("./xx_easy_server")
code = """
    push ebp
    mov ebp,esp
    push ebx
    sub esp, 0x112C4
"""
p = asm(code)
elf.write(0x080491F5-len(p),p)
elf.save("./patch")

