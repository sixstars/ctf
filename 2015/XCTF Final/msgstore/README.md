# msgstore

## writeup

### 漏洞1

`0x0000000000403E75`处的函数中可以看到下面这个读入：

```
std::istream::read((std::istream *)&std::cin, size, 4LL);std::istream::read((std::istream *)&std::cin, s, *(signed int *)size);
```

第一次读入的string的长度，由于长度没有做校验，导致很明显第二次读入会造成溢出，然后溢出的时候需要注意的是覆盖的时候要设置正确size的值，避免下面这句直接结束程序：

```v0 = std::istream::gcount((std::istream *)&std::cin);if ( v0 != *(signed int *)size )  exit(2);
```

然后实验可以发现程序在被覆盖后，函数返回前不会崩溃，于是就是裸的64位ROP链的构造即可。

### 漏洞2

待补充

### 漏洞3

待补充

### 漏洞4

待补充
