#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

def decode(l):
    return "mov dword[{}-{}],{}".format(l[2],l[1],l[0])

with open("./log","r") as f:
    data=f.read()

lines=data.split("\n")[87-1:111]

todo=map(lambda x:x[30:].split(","),lines)

print "\n".join(map(decode,todo))
