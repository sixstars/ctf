#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *
with open("sym","r") as f:
    data=f.read()


for i in range(0,len(data),2):
    if u16(data[i:i+2]) & 8 != 0:
        print chr(i/2),
