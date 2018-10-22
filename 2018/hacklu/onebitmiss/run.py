#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *
begin=0x22ee8
end=0x22ee8+0x20

s=""
for i in range(begin,end):
    r=remote("arcade.fluxfingers.net",1816)
    r.sendlineafter("[0 - 262143]:",str(i))
    r.recvuntil("]> ")
    s+=chr(int(r.recv(8),2))
    print s
    r.close()

print s

