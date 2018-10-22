#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import p64
code=p64(0x261838221c060d0a)+p64(0x2c42591c2b390f36)+\
        p64(0x392d171c262c1a36)+p64(0x0709382b07014357)+\
        p64(0x392d17131317011a)+p64(0x2e007d5c46060d0a)

code=code[:0x2e]
p=0x00
ret=[]
print hex(len(code))
for i in map(ord,code[::-1]):
    ret.append(chr(i^p))
    p=p^i

print "".join(ret)[::-1]


