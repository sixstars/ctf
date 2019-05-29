#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
from pwn import *
from pwnlib.util.iters import bruteforce

def get_cc():
    r = remote("49.4.30.253",31337)
    return r
def hash(x):
    return hashlib.sha256(x).hexdigest()


def prof(r):
    chal = r.recvline()[:-1]
    x=bruteforce(lambda x:hash(chal+x).startswith('00000'), string.ascii_letters+string.digits, length=4,method='downfrom')
    r.send(x)

data = read("./input")
while True:
    r = get_cc()
    prof(r)
    r.sendline(data)
    out = r.recvline()[:-1]
    print out
    if "Segment" in out:
        r.close()
    else:
        r.interactive()





