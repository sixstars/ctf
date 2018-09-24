# LCTF 2017

这次玩的人太少，做题数量感人……仅作简单记录

官方repo为 <https://github.com/LCTF/LCTF2017/>

以下内容来自 <https://hackmd.io/s/SykZ1Opkf>

官方repo只有exp没有思路 所以另附一份这次第一名的Nu1L的Write up

## use your ida
和看雪CTF第二题一样的思路，溢出跳到神秘代码段，然后尝试用ponce解了一下，发现可行，于是掏出angr就是干。

![](https://i.imgur.com/OrSbDOR.png)

然后根据hint，脑补为`Lctf2017`，然后出题人说“验证哪些交哪些”，最终flag为`We1come_toLctf2017B1A`


## simple blog
又是vim文件残留的问题……疯狂找代码，发现登录用admin:admin即可登录，但是需要isadmin的赋值。

看到`test_identify`的逻辑，发现这是考察`padding oracle`。不过爆破到最后一个byte的时候会出错，猜测是因为null的问题，不过乱爆就好。所用脚本见<https://gist.github.com/d867e88442d3f03222ac43adc2c2fa7b>

进去之后并没有flag，重新阅读`admin.php`，发现有`sprintf`，猜想是不是有漏洞？于是就搜了一下，很快找到了一篇资料<https://paper.seebug.org/386/>。

突破单引号后标准流程，最终payload为`http://111.231.111.54/admin.php
?title=%1$'union select 1,2,f14g from web1.key-- 
&id=1`

## 拿去当壁纸吧朋友
根据相应论文提示，google搜索`Keyless dynamic optimal multi-bit image steganography using energetic pixels`

在github上搜到相应利用程序<https://github.com/jaybosamiya/busysteg>

编译并运行，解之。
