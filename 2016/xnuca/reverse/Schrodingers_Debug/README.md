似乎弄了个thread来测debug那就先静态看看，main函数里面的sub_4016e0有点可疑有一堆检查的if判断，算了一下大概是个类似this_is_not_flag的字符串，然后跟到sub_401890里面，类似的if结构，有个(*(&dword_40413C + 1) + 12)的byte不知道，那就爆一下好了，代码如下，省略了爆破中的一堆无用输出
```
>>> d90='''C3 00 00 00 C3 00 00 00  CE 00 00 00 C4 00 00 00
C6 00 00 00 CA 00 00 00  C5 00 00 00 D0 00 00 00
C7 00 00 00 C3 00 00 00  C4 00 00 00 CF 00 00 00
CA 00 00 00 C3 00 00 00  C4 00 00 00 C9 00 00 00
C7 00 00 00 00 00 00 00'''.replace('\n',' ').replace('  ',' ')
>>> dd8='''C5 00 00 00 C4 00 00 00  C6 00 00 00 C3 00 00 00
BF 00 00 00 C4 00 00 00  BF 00 00 00 C4 00 00 00
C4 00 00 00 BF 00 00 00  C3 00 00 00 C5 00 00 00
C6 00 00 00 BF 00 00 00  C4 00 00 00 C5 00 00 00
C4 00 00 00'''.replace('\n',' ').replace('  ',' ')
>>> l=d90.split(' ')
>>> h=dd8.split(' ')
>>> for i in range(256):
	ll=[]
	hh=[]
	for j in range(17):
		ll.append((int(l[j*4],16)-3)^i)
		hh.append((int(h[j*4],16)+1)^i)
	b=False
	for ele in ll:
		if ele<0 or ele>16:
			b=True
	for ele in hh:
		if ele<0 or ele>16:
			b=True
	if b:
		continue
	aa=''
	for j in range(17):
		aa+=chr(hh[j]*16+ll[j])
	print i
	print aa

	
195
ScHr0d1ng3r_D3bUg
```
