这道题给了一个coredump文件，关键的第一步是从coredump里导出executable。通过[core2elf](https://bitbucket.org/renorobert/core2elf)这个程序可以导出可执行的elf

反编译发现程序先将输入的password每个字节都异或0x17，随后每4个字符计算一次md5，并与内置的结果比较。

因为题目说密码只有小写字母和数字，写了一个暴力破解程序：
```python
#!/usr/bin/env python3
import itertools
import hashlib

hashes=['bf2b36d56f5757c13cad80494b385e78','3fe9dbae5dc4408350500affa20074aa','1fa6770eca6b57e47a042ffe52eca8ff','1aad6b7da1122b4b5a53bf5a4d3b11b0','e7b77d9e0ab19fc9ea98154f994fccc5','75d9128cfeb61b8949664f6a067f6469','d8b0a52c64d6075017b7346140550c46','306529c7cdedfb06e27b39f7b2babf4d']
for ss in itertools.product('0123456789abcdefghijklmnopqrstuvwxyz',repeat=4):
    (a,b,c,d)=ss
    s=bytearray(a+b+c+d,'utf8')
    for i in range(0,4):
        s[i] ^= 0x17
    h=hashlib.md5()
    h.update(bytes(s))
    hashi=h.hexdigest()
    if hashi in hashes:
        print(hashi)
        print(a+b+c+d)
```

p.s. 一开始没有确认是md5，所以是把导出的elf中strcmp函数改成puts，然后不断执行该程序获得hash结果
