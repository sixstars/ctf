# from pwn import *
a=[' ']*50

# ignore check1
# a[3]='O'
# a[4]='b'
# a[5]='5'
# a[2]='_'
# a[9+2]='_'
# a[13+2]='_'
# a[30+2]='_'
# a[34+2]='_'
# a[24+2]='_'
# a[6]='0'
# a[6+1]='l'
# a[6+2]='3'
# a[6+3]='t'
# a[6+4]='e'
# a[16+2]=chr(0x64)
# a[16+1]=chr(0x6e)
# a[16]=chr(0x61)
x=0xD5A7DCD7
y=0xA1C6A7C0
a[28+13]=chr(0xd7^0x90)
a[29+13]=chr(0xdc^0x90)
a[30+13]=chr(0xa7^0x90)
a[31+13]=chr(0xd5^0x90)
a[32+13]=chr(0xc0^0x90)
a[33+13]=chr(0xa7^0x90)
a[34+13]=chr(0xc6^0x90)
a[35+13]=chr(0xa1^0x90)
a[31]='l'
a[31+1]='3'
a[31+2]='v'
a[31+3]='3'
a[31+4]='l'
# a[49]='B'

table="Unl0v4bl3S"
l_table=[0x39,0x38,0x30,0x3a,0x3b,0x3d,0x3c,0x3f,0x3e,0x31]

for i in range(10):
	a[20+i]=table[l_table[i]^0x39]

a[4]=chr(0x43)
a[5]='n'


print "".join(a)






