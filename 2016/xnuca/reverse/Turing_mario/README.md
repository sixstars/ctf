搜下文件开头的magic，虽然在github上找到个common lisp写的disasm包不过没跑起来，还有相关的[specification](http://www.cee.uma.pt/droide2/plataforma/documentation/fantom.pdf)

后来swordfeng给了个反编译后的文件就结合上面的pdf看了下，t000中的循环还算明显
```
lbl00AF:	mov	sl0014, sw0050
	index	sl0014, a00E5, sl0014
	mov	sl0018, sw0057
	mov	sl0038, sw0053
	xor	sl0038, sl0018, sl0038
	cmp	NEQ, sl0038, sl0014, sl0038
	brtst	EQ, lbl00C9, sl0038
	set	ub0068, 0x1
	jmp	lbl00CF
lbl00C9:	mov	sw0053, sw0057
	subcall	t014, ub0065
	jmp	lbl0041
```
主要这一段就是将sw0057和sw0053异或后与a00E5常量数组比较，sw0053有初值0xaf然后每次更新为sw0057的值，sw0057则跟输入有关，因为sw0057的复制是通过asl+or操作逐位进行的，可能会有类似endian的问题，所以尝试了下把输入位反过来就看到可见字符了，代码如下
```
>>> sword=[0xC9, 0x50, 0xB0, 0x60, 0x38, 0x72, 0x2, 0xA0, 0xA8, 0xE8, 0xB4, 0x4C, 0x30, 0xC8, 0xC2, 0x80, 0xF6, 0xD4, 0x80, 0xE0, 0xC2, 0xFA, 0x90, 0x1C, 0x4C, 0x34, 0x44, 0xD0, 0x80, 0xE0, 0xBA, 0x72]
>>> def rev(a):
	t=bin(a)[2:]
	t=t[::-1]
	t=t.ljust(8,'0')
	return eval('0b'+t)

>>> rev(54)
108
>>> t=0xaf
>>> a=''
>>> for i in range(32):
	tmp=sword[i]^t
	a+=chr(rev(tmp))
	t=sword[i]^t

	
>>> a
'flag{5uper_mar10_tur1ng_mAchin3}'
>>>
```
