key="abcdefghijklmnopqrstuvwxyzabcdefghi"
print(len(a))
#a='\xa6\xbd\xd2\xc1\xb7\xbc\xf8\x85{K8#|\x14\x11_S`\x0e\x08&!Fp;BH\x12!MR+}a\x01'
key=key[-1]+key[:-1]
a=[ord(x) for x in key]
z=[]
answer=[27,114,17,118,8,74,126,5,55,124,31,88,104,7,112,7,49,108,4,47,4,105,54,77,127,8,80,12,109,28,127,80,29,96]
offset=[0,-3,2,0,3,-2,1,5,1,-1,4,-1,0,2,2,5,2,-2,2,1,1,2,0,2,2,2,6,-3,-1,-1,2,-2,-1,0]
for i in range(34):
	b=a[i]
	c=a[i+1]+offset[i]
	d=b+c-2*(b&c)
	a[i+1]=d

print a==answer
