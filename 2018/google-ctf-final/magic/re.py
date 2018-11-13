#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *
context.log_level="error"
flag=list("CTF{7517f720e28c4aceb18eb1563ef01111}"+"\x00"*0x40)

def save_flag(x):
    with open("flag","w+") as f:
        f.write("".join(x))

log=open("relog","w+")

for off in range(15,32):
    pool=[]
    log.write("round:%d"%off)
    for i in "0123456789abcdef":
        tmp=list(flag)
        tmp[off+4]=i
        save_flag(tmp)
        try:
            r=process("./f -m flag.mgc -d flag".split(" "))
            p=r.recvuntil("[try softmagic 0]")
            log.write(p)
            pool.append((i,len(p.split("\n"))))
            r.close()
        except Exception as e:
            print e
            print "error %d"%off,i
            continue
    x=sorted(pool,key=lambda x:x[1],reverse=True)
    print x
    log.flush()
    flag[off+4]=x[0][0]
    print off,x[0]
    pause()
    
