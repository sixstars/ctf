## vm

既然是vm最好还是动态调吧，catch syscall write定位到0x56558d4e，（base为0x56555000，下同），下断点后发现下一次是调用fgets，再下一次计算输入长度，再下一次就输出Error了，枚举之后得到长度应该为0x1f，这样的话下一次到断点时会做内存比较，正确则说明是flag。比较对象是常量`[0xcc, 0xed, 0xf5, 0xac, 0x70, 0xa4, 0x68, 0x6c, 0xc3, 0x9c, 0x4b, 0x1b, 0x1f, 0x9f, 0xcb, 0xf2, 0x74 , 0x7d , 0x1d , 0x4e , 0xdf , 0x6c , 0x30 , 0xcb , 0x23 , 0xeb , 0x7f , 0x0e , 0x77 , 0x98 , 0x79 , 0x7e ]`，但输入似乎经过了一堆变换的样子。

那么重点就是找出这个变换了，使用watch+rwatch发现0x56556eca为write，0x565568ae为read，而且经常是2read+1write或1read+1write且第一个read的对象与write相同。跟逻辑有点困难那我们就看输入输出呗，跟了一会儿发现vm指令有点多就弄了个脚本

```
b *0x56558d4e
b *0x56558d4a
r
c
c
c
0123456789abcdefghijklmnopqrstu
c
c
disable 1 2
b *0x565568ae
b *0x56556eca
set $total=10000
set $i=0
while ($i<$total)
 c
 set $t=$eip
 if ($t==0x565568ae)
  print "R"
  set $ta=$eax
  print $ta-0x1234fd40
  set $num={char}$ta
  print $num
  end
 if ($t==0x56556eca)
  print "W"
  set $tc=$ecx
  print $tc-0x1234fd40
  print $eax
  end
 end
```

修改输入多试了几次得到所有vm指令输入输出若干，然后就猜指令喽，使用下面的脚本产生相对应的逆指令，无法识别时让程序输出然后自己改代码，以及给这团东西debug真是可怕……

```
def uin(x):
        return 's['+str(x)+']'

f1=open('vmout1')
fs=[open('vmout'+str(i)) for i in range(2,6)]
l1=f1.readline()
ln=0
while (l1!=''):
        a1=int(f1.readline(),16)
        v1=int(f1.readline(),16)
        if f1.readline().find('W')==-1:
                ln+=9
                a2=int(f1.readline(),16)
                v2=int(f1.readline(),16)
                f1.readline()
                r=int(f1.readline(),16)
                vr=int(f1.readline(),16)
                ba1=[]
                bv1=[]
                ba2=[]
                bv2=[]
                br=[]
                bvr=[]
                for f2 in fs:
                        f2.readline()
                        ba1.append(int(f2.readline(),16))
                        bv1.append(int(f2.readline(),16))
                        f2.readline()
                        ba2.append(int(f2.readline(),16))
                        bv2.append(int(f2.readline(),16))
                        f2.readline()
                        br.append(int(f2.readline(),16))
                        bvr.append(int(f2.readline(),16))
                noto=True
                t=False
                if noto==True and v1^v2==vr:
                        t=True
                        for i in range(4):
                                if (bv1[i]^bv2[i])!=bvr[i]:
                                        t=False
                                        break
                if noto==True and t==True:
                        print uin(r)+'='+uin(a1)+'^'+uin(a2)
                        noto=False
                if noto==True and (v2-v1)&0xff==vr:
                        t=True
                        for i in range(4):
                                if (bv2[i]-bv1[i])&0xff!=bvr[i]:
                                        t=False
                                        break
                if noto==True and t==True:
                        print uin(r)+'=('+uin(a2)+'-'+uin(a1)+')&0xff'
                        noto=False
                if noto==True and (v1-v2)&0xff==vr:
                        t=True
                        for i in range(4):
                                if (bv1[i]-bv2[i])&0xff!=bvr[i]:
                                        t=False
                                        break
                if noto==True and t==True:
                        print uin(r)+'=('+uin(a1)+'+'+uin(a2)+')&0xff'
                        noto=False
                if noto==True and (v1+v2)&0xff==vr:
                        t=True
                        for i in range(4):
                                if (bv1[i]+bv2[i])&0xff!=bvr[i]:
                                        t=False
                                        break
                if noto==True and t==True:
                        print uin(r)+'=('+uin(a1)+'-'+uin(a2)+')&0xff'
                        noto=False
                if noto==True:
                        print 'what?'
                        print v1,v2,vr
                        print bv1,bv2,bvr
                        exit()
        else:
                ln+=6
                r=int(f1.readline(),16)
                vr=int(f1.readline(),16)
                ba1=[]
                bv1=[]
                br=[]
                bvr=[]
                for f2 in fs:
                        f2.readline()
                        ba1.append(int(f2.readline(),16))
                        bv1.append(int(f2.readline(),16))
                        f2.readline()
                        br.append(int(f2.readline(),16))
                        bvr.append(int(f2.readline(),16))
                noto=True
                if noto==True:
                        t=True
                        eq=vr^v1
                        for i in range(4):
                                if bvr[i]^bv1[i]!=eq:
                                        t=False
                                        break
                if noto==True and t==True:
                        print uin(r)+'='+uin(a1)+'^'+str((vr^v1))
                        noto=False
                if noto==True:
                        t=True
                        eq=(vr-v1)&0xff
                        for i in range(4):
                                if (bvr[i]-bv1[i])&0xff!=eq:
                                        t=False
                                        break
                        if noto==True and t==True:
                                print uin(r)+'=('+uin(a1)+'-'+str((vr-v1)&0xff)+')&0xff'
                                noto=False
                if noto==True:
                        print 'what?'
                        print v1,vr
                        print bv1,bvr
                        exit()
        l=f1.readline()
```

然后执行一遍

```
f=open('vmcode_r')
c=f.readlines()
s=[0xcc, 0xed, 0xf5, 0xac, 0x70, 0xa4, 0x68, 0x6c, 0xc3, 0x9c, 0x4b, 0x1b, 0x1f, 0x9f, 0xcb, 0xf2, 0x74 , 0x7d , 0x1d , 0x4e , 0xdf , 0x6c , 0x30 , 0xcb , 0x23 , 0xeb , 0x7f , 0x0e , 0x77 , 0x98 , 0x79 , 0x7e ]
for i in range(len(c))[::-1]:
        exec(c[i])
print s
ans=''
for ch in s:
        ans+=chr(ch)
print ans
```

由于样例的关系得到的vm指令可能有多解，加到5组样例后感觉大概能看了，就稍微调了下指令的优先级，然后就得到flag了
`0ctf{Mipsel_Virtual_Machine_><}`
