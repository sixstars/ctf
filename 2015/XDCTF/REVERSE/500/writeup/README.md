注册机程序，给定机器码要求key，在string里可以发现openssl之类字样。

这题前半部分是队友看的，发现程序动态hook了GetDlgTextA，在其中首先检查位数是否48位，然后只包含0-9,A-F，接着进行hex解码后，扔到某个函数里处理后，前32位与机器码比较，后16位均为08（其实前部分是机器码移动2位再与0xe4异或后再比较的，还用了xmm0，不过那都是细节）。

关键就是前面的“某个函数”了，多试几次发现输入输出以64bit为一个块单位，结合字符串“libdes...”“解密之前”猜测该函数对输入使用des进行了解密，然后尝试找可疑的des key，试了好几处发现函数开头的赋值有点奇怪，验证发现des key就是e1723b0b73f4c641，要记得大小端转换。

des操作采用pycrypto库，代码段如下：

c是用key和mode_ecb初始化后的des

```python
>>> ss='F89AE772A6F990306EB0E82448435BFF'
>>> t=ss.decode('hex')
>>> t1=''
>>> for ch in t:
...     t1+=chr(ord(ch)^0xe4)
...
>>> t1
'\x1c~\x03\x96B\x1dt\xd4\x8aT\x0c\xc0\xac\xa7\xbf\x1b'
>>> t1.encode('hex')
'1c7e0396421d74d48a540cc0aca7bf1b'
>>> ss='1c7e0396421d74d48a540cc0aca7bf1b0808080808080808'
>>> ss=ss.decode('hex')
>>> c.encrypt(ss).encode('hex')
'9eea87758a647e5d74a376cd6281cfb5970bb701caf237f3'
>>> s=c.encrypt(ss).encode('hex')
>>> s.upper()
'9EEA87758A647E5D74A376CD6281CFB5970BB701CAF237F3'
```
