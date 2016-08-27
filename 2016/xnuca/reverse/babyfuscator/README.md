放假在家手头没有angr，反正flag不同位互不影响，就用不那么优雅的方法一个个爆了
```
>>> ans='X'*32
>>> def v17(x):
	return (x ^ 0x10) + 10) ^ 0x12;
SyntaxError: invalid syntax
>>> x=1
>>> (x ^ 0x10) + 10) ^ 0x12;
SyntaxError: invalid syntax
>>> def x0(x):
	v17=((x ^ 0x10) + 10) ^ 0x12;
	v3 = ((((((v17 + 1) ^ 0x1B) + 6) ^ 0x39) + 8) ^ 0x29) + 8;
	return ((v3 ^ 0x3B) + 4) ^ 0xA

>>> for i in range(256):
	if x0(i)==216:
		print i,

		
119
>>> ans[0]=chr(119)

Traceback (most recent call last):
  File "<pyshell#13>", line 1, in <module>
    ans[0]=chr(119)
TypeError: 'str' object does not support item assignment
>>> ans=['X']*32
>>> ans[0]=chr(119)
>>> def x1(x):
	v18=((x ^ 5) + 10) ^ 0x16;
	v12 = ((v18 + 8) ^ 0x2F) + 9;
	v7 = (v12 ^ 0x32) + 10;
	return ((((v7 ^ 0xB) + 6) ^ 0x2B) + 6) ^ 6)
SyntaxError: invalid syntax
>>> def x1(x):
	v18=((x ^ 5) + 10) ^ 0x16;
	v12 = ((v18 + 8) ^ 0x2F) + 9;
	v7 = (v12 ^ 0x32) + 10;
	return (((v7 ^ 0xB) + 6) ^ 0x2B) + 6) ^ 6)
SyntaxError: invalid syntax
>>> def x1(x):
	v18=((x ^ 5) + 10) ^ 0x16;
	v12 = ((v18 + 8) ^ 0x2F) + 9;
	v7 = (v12 ^ 0x32) + 10;
	return ((((v7 ^ 0xB) + 6) ^ 0x2B) + 6) ^ 6

>>> for i in range(256):
	if x1(i)==132:
		print i,

		
107
>>> ans[1]=chr(107)
>>> def x2(x):
	v18 = ((x ^ 0x26) + 10) ^ 0x14;
	v7 = ((((v18 + 7) ^ 7) + 7) ^ 9) + 5;
	return ((((v7 ^ 0x3D) + 6) ^ 0x31) + 5) ^ 0xC

>>> for i in range(256):
	if x2(i)==40:
		print i,

		
54
>>> ans[2]=chr(54)
>>> def x3(x):
	v18 = ((x ^ 0x2F) + 5) ^ 0x29;
	v14 = (v18 + 10) ^ 0x1F;
	return (((((((v18 + 10) ^ 0x27) + 6) ^ 0x31) + 9) ^ 0x26) + 8) ^ 0x32

>>> for i in range(256):
	if x3(i)==12:
		print i,

		
48
>>> ans[3]=chr(48)
>>> def x4(x):
	v18 = x ^ 0x1F;
	v7 = ((((v18 + 9) ^ 0x21) + 4) ^ 0x27) + 9;
	return ((((v7 ^ 0x2D) + 7) ^ 0x19) + 9) ^ 0x39

>>> for i in range(256):
	if x4(i)==52:
		print i,

		
56
>>> ans[4]=chr(56)
>>> def x5(x):
	v17 = (x + 9) ^ 0x26;
	v3 = ((((((v17 + 9) ^ 0x10) + 4) ^ 0x32) + 1) ^ 5) + 1;
	return ((v3 ^ 0xA) + 7) ^ 0x12

>>> for i in range(256):
	if x5(i)==94:
		print i,

		
116
>>> ans[5]=chr(116)
>>> def x6(x):
	return ((((((((((x ^ 0x17) + 6) ^ 0x27) + 1) ^ 0x26) + 6) ^ 1) + 2) ^ 0x16) + 7) ^ 0x1C

>>> for i in range(256):
	if x6(i)==45:
		print i,

		
56
>>> ans[6]=chr(56)
>>> def x7(x):
	v19 = x ^ 0x1A;
	v11 = (((((v19 + 8) ^ 9) + 3) ^ 0x25) + 4) ^ 0x30;
	return ((((v11 + 7) ^ 0x24) + 5) ^ 0x2F) ^ 0x2B

>>> for i in range(256):
	if x7(i)==79:
		print i,

		
52
>>> ans[7]=chr(52)
>>> def x28(x):
	v19 = x ^ 0x30;
	v10 = (((((v19 + 5) ^ 0x11) + 8) ^ 0x13) + 8) ^ 0x21;
	v2 = (((v10 ^ 0x35) + 4) ^ 0x19) + 7;
	return v2 ^ 0x12

>>> for i in range(256):
	if x28(i)==111:
		print i,

		
120
>>> ans[28]=chr(120)
>>> def x29(x):
	v19 = x ^ 0x11;
	v11 = (((((v19 + 9) ^ 6) + 1) ^ 0x15) + 1) ^ 0x3E;
	v4 = ((v11 + 9) ^ 0xF) + 9;
	return ((v4 ^ 0x2D) + 5) ^ 2

>>> for i in range(256):
	if x29(i)==237:
		print i,

		
97
>>> ans[29]=chr(97)
>>> def x30(x):
	v18 = ((x ^ 6) + 9) ^ 0x19;
	v14 = (v18 + 6) ^ 0x2C;
	v6 = (((v14 + 7) ^ 0xF) + 10) ^ 0x24;
	return (((v6 + 7) ^ 8) + 7) ^ 0x2E

>>> for i in range(256):
	if x30(i)==187:
		print i,

		
101
>>> ans[30]=chr(101)
>>> def x31(x):
	return ((((((((((((x ^ 8) + 7) ^ 0x2C) + 6) ^ 0x3C) + 3) ^ 0x17) + 8) ^ 0x30) + 6) ^ 0x3C) + 6) ^ 0x17

>>> for i in range(256):
	if x31(i)==56:
		print i,

		
56
>>> ans[31]=chr(56)
>>> def x8(x):
	v18 = ((x ^ 0xC) + 1) ^ 0x34;
	v14 = (v18 + 1) ^ 6;
	v13 = v14 + 8;
	return (((((((v14 + 8) ^ 0x27) + 8) ^ 0x3B) + 2) ^ 0x23) + 3) ^ 0x16

>>> for i in range(256):
	if x8(i)==76:
		print i,

		
110
>>> ans[8]=chr(110)
>>> def x9(x):
	v17 = ((x ^ 0xA) + 4) ^ 0x3D;
	return (((((((((v17 + 10) ^ 0x37) + 1) ^ 0x19) + 1) ^ 0x23) + 9) ^ 0x38) + 4) ^ 0x29

>>> for i in range(256):
	if x9(i)==67:
		print i,

		
97
>>> ans[9]=chr(97)
>>> def x10(x):
	v20 = x) ^ 0xD;
	
SyntaxError: invalid syntax
>>> def x10(x):
	v20 = x ^ 0xD;
	v17 = (v20 + 5) ^ 0x3A;
	return (((((((((v17 + 6) ^ 0x28) + 5) ^ 0x1B) + 1) ^ 0x1D) + 7) ^ 0x39) + 3) ^ 0x36

>>> for i in range(256):
	if x10(i)==82:
		print i,

		
111
>>> ans[10]=chr(111)
>>> def x11(x):
	v18 = ((x ^ 0x20) + 3) ^ 0x3C;
	return (((((((v18 + 10) ^ 0x3A) + 1) ^ 3) + 11) ^ 0x36) + 7) ^ 0x29

>>> for i in range(256):
	if x11(i)==209:
		print i,

		
99
>>> ans[11]=chr(99)
>>> def x12(x):
	v19 = x ^ 9
	v11 = (((((v19 + 3) ^ 0x2F) + 1) ^ 0x38) + 1) ^ 0x3F;
	v8 = v11 + 8;
	return ((v8 ^ 9) + 6) ^ 0x21

>>> for i in range(256):
	if x12(i)==107:
		print i,

		
101
>>> ans[12]=chr(101)
>>> def x13(x):
	v18 = ((x ^ 0x2C) + 9) ^ 0x35;
	v12 = (v18 + 7) ^ 0x29;
	v5 = ((((v18 + 7) ^ 0x21) + 8) ^ 0xA) + 6;
	return ((v5 ^ 0x26) + 10) ^ 0x2D

>>> for i in range(256):
	if x13(i)==81:
		print i,

		
54
>>> ans[13]=chr(54)
>>> def x14(x):
	v17 = x ^ 0x1F;
	v3 = ((((v17 + 5) ^ 0x3A) + 2) ^ 0x27) + 2;
	return ((v3 ^ 0x1B) + 9) ^ 0x16

>>> for i in range(256):
	if x14(i)==61:
		print i,

		
48
>>> ans[14]=chr(48)
>>> def x15(x):
	v19 = x ^ 0x10;
	v15 = (((v19 + 10) ^ 0x14) + 7) ^ 3
	v11 = (v15 + 1) ^ 0x1E;
	v4 = ((v11 + 9) ^ 0x1A) + 7;
	return ((v4 ^ 0x24) + 2) ^ 3

>>> for i in range(256):
	if x15(i)==234:
		print i,

		
116
>>> ans[15]=chr(116)
>>> def x16(x):
	v18 = ((x ^ 4) + 3) ^ 7;
	v12 = v18 + 15;
	v5 = ((((v18 + 15) ^ 0x33) + 6) ^ 0x1C) + 7;
	return ((v5 ^ 0x2A) + 8) ^ 0x2D

>>> for i in range(256):
	if x16(i)==98:
		print i,

		
56
>>> ans[16]=chr(56)
>>> def x17(x):
	v18 = ((x ^ 0x20) + 3) ^ 0x1D
	v16 = v18 + 9;
	v9 = ((((v18 + 9) ^ 0x3F) + 8) ^ 8) + 10;
	return ((((v9 ^ 0x23) + 3) ^ 0x11) + 5) ^ 0x28

>>> for i in range(256):
	if x17(i)==101:
		print i,

		
99
>>> ans[17]=chr(99)
>>> def x18(x):
	v18 = ((x ^ 0x22) + 5) ^ 0x12;
	v14 = (v18 + 8) ^ 0xA;
	return (((((((v18 + 8) ^ 0x25) + 1) ^ 0x29) + 4) ^ 0x1F) + 4) ^ 0xF

>>> for i in range(256):
	if x18(i)==72:
		print i,

		
120
>>> ans[18]=chr(120)
>>> def x19(x):
	v19 = x ^ 0x11;
	v18 = (v19 + 6) ^ 0x2E;
	v16 = v18 + 7;
	return ((((((((v16 ^ 0xB) + 6) ^ 0x24) + 9) ^ 0x1E) + 4) ^ 0x2A) + 5) ^ 0x21

>>> for i in range(256):
	if x19(i)==98:
		print i,

		
48
>>> ans[19]=chr(48)
>>> def x20(x):
	v20 = x ^ 0x3C;
	return ((((((((v20 + 4) ^ 0x27) + 3) ^ 4) + 9) ^ 3) + 4) ^ 0x36) ^ 0x27

>>> for i in range(256):
	if x20(i)==150:
		print i,

		
111
>>> ans[20]=chr(111)
>>> def x21(x):
	v18 = ((x ^ 0x2C) + 1) ^ 0x28;
	v13 = (v18 + 5) ^ 0x27;
	return (((((v13 ^ 0x3A) + 7) ^ 1) + 10) ^ 0x2F) ^ 0x1B

>>> for i in range(256):
	if x21(i)==69:
		print i,

		
56
>>> ans[21]=chr(56)
>>> def x22(x):
	v17 = ((x ^ 0x33) + 4) ^ 0x38;
	return (((((((((v17 + 5) ^ 0x3A) + 7) ^ 0x1A) + 7) ^ 0xC) + 2) ^ 0x28) + 5) ^ 0x2A

>>> for i in range(256):
	if x22(i)==101:
		print i,

		
50
>>> ans[22]=chr(50)
>>> ans[27]
'X'
>>> def x23(x):
	v18 = x ^ 0x23;
	v9 = ((((v18 + 3) ^ 9) + 3) ^ 0x1B) + 9;
	return ((((v9 ^ 0x11) + 2) ^ 0x3A) + 8) ^ 0xC

>>> for i in range(256):
	if x23(i)==115:
		print i,

		
104
>>> ans[23]=chr(104)
>>> def x24(x):
	v17 = ((x ^ 0x29) + 2) ^ 0x18;
	return (((((((v17 + 3) ^ 8) + 5) ^ 0x22) + 10) ^ 0x22) + 5) ^ 0x3A

>>> for i in range(256):
	if x24(i)==98:
		print i,

		
114
>>> ans[24]=chr(114)
>>> def x25(x):
	v19 = x ^ 0x2B;
	v15 = (((v19 + 1) ^ 0x1F) + 7) ^ 2;
	return (((((((v15 + 5) ^ 0x20) + 5) ^ 0x37) + 4) ^ 8) + 9) ^ 0x1F

>>> for i in range(256):
	if x25(i)==129:
		print i,

		
116
>>> ans[25]=chr(116)
>>> def x26(x):
	v19 = x ^ 9;
	v11 = (((((v19 + 3) ^ 0x35) + 3) ^ 0x2E) + 10) ^ 0xE;
	v2 = ((((v11 + 8) ^ 0x1B) + 3) ^ 0x1E) + 10;
	return v2 ^ 0x34

>>> for i in range(256):
	if x26(i)==181:
		print i,

		
111
>>> ans[26]=chr(111)
>>> def x27(x):
	 v19 = x ^ 0x36;
	 v11 = (((((v19 + 3) ^ 0x14) + 2) ^ 0x3B) + 7) ^ 0x24;
	 v8 = v11 + 9;
	 return ((((v8 ^ 0x39) + 3) ^ 0x36) + 3) ^ 0x16

	
>>> for i in range(256):
	if x27(i)==171:
		print i,

		
120
>>> ans[27]=chr(120)
>>> ans
['w', 'k', '6', '0', '8', 't', '8', '4', 'n', 'a', 'o', 'c', 'e', '6', '0', 't', '8', 'c', 'x', '0', 'o', '8', '2', 'h', 'r', 't', 'o', 'x', 'x', 'a', 'e', '8']
>>> aa=''
>>> for ch in ans:
	aa+=ch

	
>>> aa
'wk608t84naoce60t8cx0o82hrtoxxae8'
>>> 
```
