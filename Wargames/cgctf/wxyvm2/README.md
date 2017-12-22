这道题代码量巨大，IDA表示无法显示……

但仔细观察一番后，发现是一条直线执行一大段VM代码后，进入了一个逐位比较，VM代码中没有任何跳转。

那么就很容易想到是侧信道攻击了。

要了解侧信道攻击，推荐这篇文章 <https://servers.ustclug.org/2014/05/fix-freeshell-side-channel-attach/>

用ncat启pin，返回指令数目，用pwntools负责攻击，经过简单的几次尝试可以发现每正确一位，指令数目-1。

那么脚本如下：

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *


context.log_level = 'error'
cur = 'nctf{th3_vM_w1th0ut_dAta'
cur_ = 269637

pt = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm_}1234567890'

while len(cur) < 24:
    for i in pt:
        r = remote('127.0.0.1', 4444)
        tmp = cur + i
        tmp = tmp.ljust(25, '.')
        r.sendline(tmp)
        r.recvuntil('Count ')
        ins = r.recvuntil('\n').strip()
        ins = int(ins)
        print tmp, ins
        if ins == cur_ - 1:
            cur += i
            cur_ -= 1
            break
        r.close()

print cur + '}'
print 'ok'
```

注意我没有爆最后一位，因为最后成功的指令数目应该是不是上一轮-1。

这道题可以用作pintool的练习题。
