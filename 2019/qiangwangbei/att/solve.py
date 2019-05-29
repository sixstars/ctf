#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
flag= "0401575e56000c0207005b535502015157565303525357035401015107020252".decode("hex")
token = "4e2805940cbe16d567d3fd2a23d20f7a"
s=""
for i in range(0,len(flag)):
    s+=chr(ord(flag[i])^ord(token[i%len(flag)]))

print s
