#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from struct import pack,unpack

def p8(n):
    return pack("<B",n)

def p16(n):
    return pack("<H",n)

def p32(n):
    return pack("<I",n)

def p64(n):
    return pack("<Q",n)

def u8(s):
    return unpack("<B",s)[0]

def u16(s):
    return unpack("<H",s)[0]

def u32(s):
    return unpack("<I",s)[0]

def u64(s):
    return unpack("<Q",s)[0]
