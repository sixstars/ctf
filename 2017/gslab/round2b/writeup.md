PC、Android 程序逻辑应该差不多，这里以 Android 为例。

## 学生组

打开首先看到竟然有个 dll，差点就以为下错题了，厉害了，Android 题给 dll。

打开 main 后大概扫了下，看到不少 mono 字样，看起来就是这玩意当做运行时了。
上网查了下，貌似是个 .Net 的三方运行时，gg，对 .Net 和 C# 那一套真是完全没了解，需要从头学起了。

那么首先这个程序是自己带着 mono 静态编译了的程序咯，mscorlib.dll 是 .Net 的基础库咯。
看起来又是个可以练习下 FLARE 的好机会，正好最近在学着自己用。

不过貌似 mono 版本没看到在哪里，以及折腾一份 Android 上的 mono 看起来好麻烦的样子。
那还是对着 mono 源代码随便先看看好了。

首先 init array 中有个函数 0x0000A024，看了眼是拿 main 函数的代码算校验，应该是防止在 main 上下断点用的咯。
然后 main 开始的地方新开了个线程运行 0x0000A15C，各种 ptrace，看其实是不停的把 stop 住的程序启动起来，那也是个反调咯。
接着对 0x36F000 处的数据做了个 xor 的变换，然后进了 0xB925C 处，对于长度大小在 0x1400 到 0x17EC 中的数据又做了个 xor 的变换。
接下来调用的 0x000B8990 就是 do_mono_image_load 了（随便点，看到 assert 和 error 的报错去 mono 代码中定位反向一路走上来比较方便识别）。

于是把 0x36F000 处的数据拉下来解密好，果然 MZ 打头，看起来没什么问题，然而交给 monodis 报错，
为防止提错了，去 win 版题目中也提取了一下，动态跑起来 IDA 中也提了下，都确认没问题。
这下真是尴尬了，难道要还要修复 PE，这 PE 也不熟悉啊，gg。

仔细再看看，0xB925C 原来就是 mono_image_open_from_data_with_name，不过被篡改加上了那段 xor，这么说来，难道 do_mono_image_load 里面也被改了，这是要开个 bindiff 的节奏啊……
再查查资料发现好像这种修改做加解密 mono_image_open_from_data_with_name 好像很常见，那看来改里面东西的可能性不大了……

想起来程序有一堆 logcat 的调用，差点忘了，看看 logcat 发现竟然也是输出了一堆 `Unknown heap type:` 的报错。
这什么情况，程序应该是正常运行了啊，难道说这些错误可以忽视，但 monodis 和 ILSpy 没有去忽视。

010 跑了下模板，发现竟然跑挂了，什么 Signature 不对，
再找了个 HelloWorld 的跑了下，发现 NtHeader Signature 那里应该是 0x4550，而我们手里的是 0x1004550，那就改掉咯，再跑模板就没错了。

那么现在由于程序只调用了这个 PE 里面什么 SayHello 之类的函数，那么有可能就是其它无关部分就被破坏了，导致 monodis 没法愉快的跑，那去自己把 IL 提出来好了。
好不容易借了个 Windows 装了 ildasm，发现还是报错：未能打开元数据，gg。
仔细再看看 monodis 的报错 `* Assertion at image.c:540, condition 'image->heap_guid.data' not met`，
于是再去搜着看 mono 源代码和 IDA 对比，关键看起来就在 load_metadata_ptrs 里面了，`Unknown heap type` 也是这里面报的错。

拿着文件一点点对比，发现头上一个关于 heap 的信息的个数不对，0x105 明细太大，应该是 0x5，
然后有个叫 `#Strings` 信息被篡改成了 `#String`，都改好后 monodis 可以正常出结果了，不过 ILSpy 还是报错。

懒得看为什么 ILSpy 继续挂了，直接看 IL 好了，反正也就几百行。
首先很明显目标是一个 `default void EncryptDataFile ()` 函数，函数读入 `areyouok.png` 文件，
调用 `unsigned int8[] class encrypt.MyClass::Encrypt(unsigned int8[])`，写到 `areyouok_encrypted` 文件中。
再看 Encrypt 函数……

看到一半的时候突然想到，ILSpy 直接跑不了这个，估计是因为还有些要修的地方，但我们既然有 IL 了，可以直接自己编译一个 exe，这样应该不用修了。
直接 ilasm 会报 `Error : No entry point found.`，大概是由于 dll 没入口吧。
不管那么多，直接将之前的 HelloWorld 拼在一起，编译好交给 ILSpy，果然成功打开，整个世界都清晰了。

Encrypt 函数做了个分组加密，分组大小 8 个 byte，给的几个常亮都搜不到现成算法。
看了下感觉如果直接要写逆向算法好像会比较烦，仔细观察发现其实还有个隐藏的常量：
`uint num4 = Convert.ToUInt32(Math.Floor((Math.Pow(5.0, 0.5) - 1.0) * Math.Pow(2.0, 31.0)));`，
固定为 0x9e3779b9，于是搜到 XTEA 算法，对比下代码果然没错。

貌似直接改反编译的代码中 encrypt 的逻辑变成 decrypt 会很方便，不过是在不熟悉 .Net 这一套，还是找 Python 的实现好了。
key 是 `[363609949, 512121596, 1703126449, 1423373290]`，IV 是 `[363609949, 1703126449]`，mode 是 CBC。
然而，找来的 Python 版半天都解不对，不想折腾了，于是回去对着 Encrypt 抄了个 C# 的 Decrypt，成功解密得到图片。

打开图片显示 `你了解图片格式吗~`，首先扔 stegsolve 发现没什么特别的。
010 打开很明显可以看到第五个 chunk 损坏了，sRGB 已经出现过，同时 sRGB 的 data length 也不能是 0x116，所以 type 肯定有问题。
实在是想不出该改成什么，于是假设 crc 是对的（讲道理的话 crc 的值确实挺奇怪的，但毕竟 crc 是可以构造的），暴力一下这四位，一个解都找不到……

于是这道题就变成脑洞题了，心中问候出题人无数遍后，终于脑洞出来脑洞打开，想出来了，
不再企图对这个 PNG 做修复，而是直接把损坏的 chunk 中的 data 提取出来扔掉 PNG 分析。
data 开头有个 0x116 的小端序，然后数据一堆 0xff 很有规律，自动脑补出 BMP，于是把提取的数据头两个字节改成 BM 头即可看到最终图片。

## 社会组

首先和学生组一样把数据拉下来解密得到 PE，一模一样的三个地方修复一下。
交个 monodis 发现跑不了，观察下发现指令很奇怪，和学生组对照了一下，貌似是指令的 opcode 全部被增加了 0xf。
改了下 monodis 源代码，编译好后反汇编成功，但是结果看起来就有些不太对，那这下感觉是改了指令解析的代码。

翻来覆去的去找解析 opcode 的代码，终于在折腾 N 小时后，发现了 mono_opcodes 数组，一看，很明显 opcode 顺序不对，
突然就发现自己智障了，这明显不是改了代码，改的是 opcode 的定义，竟然一直没有反应过来。

于是修改 monodis 源代码中 opcode 定义，0xB3-0xC1 换成 0x0-0xE，0x0-0xB2 换成 0xF-0xC1，其余不变。

```python
fp = open('opcode.def')
res = [fp.readline()]
for i in xrange(0xB3):
    row = fp.readline()
    s_row = row.rsplit(',', 2)
    res.append('{}, {:#X},{}'.format(s_row[0], int(s_row[1], 16) + 0xF, s_row[2]))
for i in xrange(0xF):
    row = fp.readline()
    s_row = row.rsplit(',', 2)
    res.insert(1 + i, '{}, 0x{:02X},{}'.format(s_row[0], int(s_row[1], 16) - 0xB3, s_row[2]))
res.append(fp.read())
fp.close()
fp = open('modified-opcode.def', 'w')
fp.writelines(res)
fp.close()
```

替换好之后解码成功，按照和之前一样的方式重编译后交给 ILSpy 拿到 C#，发现和之前的代码基本一样，只是换了个加密的 key、IV。
于是改了下解密，得到 `areyouok.png` 和学生组的一样，直接提取 chunk data 修改为 BM 头即可。
