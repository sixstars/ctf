#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
from pwn import *
code=open("./re.asm","r").read()
code=asm(code,arch="amd64")
open("bin","w+").write(code)

