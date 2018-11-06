#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
from pool import array
begin=0x00402626
for i in range(0x132):
    tmp=(array[i]&0xff)^Byte(i+begin)
    PatchByte(i+begin,tmp)

