

def trans(x,y):
	return (x&y)^0xffffffff

table='\x10\x18C\x14\x15G@\x17\x10\x1dK\x12\x1fIH\x18ST\x01WQS\x05VZ\x08X_\n\x0cX\t'

def recver(x,x140):
	x143=x
	x141=trans(x140,x)
	x142=trans(x141,x140)
	x144=trans(trans(x143,x141),x142)
	return x144

s=""
for p in range(0x20):
	x=0x20+p
	for i in range(0x100):
		if recver(i,x)&0xff==ord(table[p]):
			s=s+chr(i)
print s
