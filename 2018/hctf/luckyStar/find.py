#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

raw = open("./raw","r").read()
code = open("./code","r").read()

f = open("byte_xor","w+")

for i in range(len(raw)):
    f.write(str(ord(raw[i])^ord(code[i]))+"\n")

f.close()

