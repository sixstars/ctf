#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from subprocess import call

import  string
pool=string.printable

s="2bcdKPZ_"
a=[' ']*49
a[5]='n'

for p in s:
    for q in pool:
        a[3]=p
        a[4]=q
        ret=call(["./challenge.bak","".join(a)])
        if ret!=1:
            print p,q,ret







