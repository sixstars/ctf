首先 Java 层看一眼什么都没有，又是全在 native。

顺着 `Java_com_qq_gslab_regme_MainActivity_checkReg` 往下看，第一个检查是 `CRegCheck::is_user_name_legal` 检查 key。
可以发现首先用 `-` 做分隔符 split，split 之后总长度大概应该是 32，每个字符都是 hex digits。

然后 `CRegCheck::get_formula_param` 会将 key 转换成 4 个长整数，由于 C++ 的代码，所以无用逻辑比较多，耐着性子看下其实就可以了。
不过突然心血来潮，打算练习下 angr 的使用，于是看完后又用 angr 写了一份代码来做这个转换。

### standard

接着对于 standard 难度，会对输入 code 做个 `CBase64::base64_decode`，然后实际试试会发现这不是标准 base64。
看看代码首先发现换了 base64 的表，尝试了下还是不对。
仔细再看看代码，发现每个字符找到序号后，对序号 `x` 做了个 `x ^ (x >> 4)`，可以理解为把表又四个四个一组的换了一下。
于是写了份代码置换下表：

```python
table = "OPWvYny#Nopz0$HI34QRSG@dJKq7fghD9Zi*kAB8rsFu56L&Ca^2tTUVEewxlm+/"
new_table = ''
for i in xrange(4):
    s = table[16 * i:][:16]
    tzb = [''] * 16
    for idx, c in enumerate(s):
        tzb[idx ^ i] = c
    new_table += ''.join(tzb)
```

找份 base64 实现将表换掉后即可正常编码解码。

然后 code 解码得到的串需要是 16 位，并看做两个长整数，此时我们共得到 6 个长整数。

程序最后通过 `is_tangent` 对这 6 个数做了一个校验。
然而函数名看不懂，整个代码也就两句话，其实相当于是用 2 个方程的二元二式方程组求解了（code 的两个数作为未知数）。
大概可以转化成 `(x - a) ^ 2 = b (mod 2^64)`，即做个模 `2^64` 的开方，从二进制低位往高位一位位算好了。
不过偷个懒，直接上 z3 解好了，虽然慢了点，总归还是可以算的。

一组 key, code:
```
0123-4567-89ab-cdef-0123-4567-89ab-cdef
4+O^LOauSky#DBKnhozvJi==
```

### advance

对于 advance，其实就是把 code 转成 2 个数的方法变了下，用 RSA 解密代替了 `CBase64::base64_decode`。
RSA 随机生成的 key，不过随机的种子是用的 `CRegCheck::get_rsa_key_seed` 算出来的，
这个函数和 `CRegCheck::get_formula_param` 比较类似，用 angr 跑一下好了。
这样在随机种子确定的情况下，随机生成的 RSA 的 key 其实是确定的。

仔细看下 `RSA::RSAKey` 中间的代码，会发现随机 RSA 结构体大致如下：

```
0xBEAAB538 +0 p 9236592661
0xbeaab6c8 +400 q 19789050901
0xbeaab858 +800 N 182783402320332037561
0xbeaab9e8 +1200 d 103692016626576834529
0xbeaabb78 +1600 e 89569
0xbeaabd08 +2000 phi(N) 182783402291306394000
0xbeaabe98 +2400 p - 1 9236592660
0xbeaac028 +2800 q - 1 19789050900
```

特别需要注意的是，程序对大整数的表示形式，采用 `int[100]`，最高位为长度。
程序中静态写死了 p 长度 10, q 长度 11，e 长度 5。

同时输入的 code 经过 `CBase64::base64_decode` 作为密文。
密文是分段的，每一段解密得到一个字符。
然后每一段密文的格式好像是 `符号位 + 长度 + 数`，其中长度和数十进制表示倒着写成字符串。
即密文 28 最终写作 `0 20 28`。

**未完待续** （有空再补）
