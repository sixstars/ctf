这道题代码量巨大，IDA表示无法显示……

但仔细观察一番后，发现是一条直线执行一大段VM代码后，进入了一个逐位比较，VM代码中没有任何跳转。

那么就很容易想到是侧信道攻击了。

要了解侧信道攻击，推荐这篇文章 <https://servers.ustclug.org/2014/05/fix-freeshell-side-channel-attach/>

用ncat起pin返回指令数目，用pwntools负责攻击，经过简单的几次尝试可以发现每正确一位，指令数目-1。

当然你可以用subprocess来负责处理输入输出，也许能带来一些性能上的提升？不过通过socket来处理我个人觉得写起来更简单。

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

注意我没有爆最后一位，因为最后成功的指令数目应该不是上一轮-1。

这道题可以用来讲解pintool。

另外有 <https://github.com/blankwall/Python_Pin> 可以用来写攻击脚本，留作习题。
