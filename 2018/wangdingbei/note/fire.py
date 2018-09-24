#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
from pwn import *

def exploit(ip):
    r=remote("127.0.0.1",9999)
    flag=r.recvline()[:-1]
    r.close()
    return flag
