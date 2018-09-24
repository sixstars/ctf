```
>>> c='805eed80cbbccb94c36413275780ec94a857dfec8da8ca94a8c313a8ccf9'.decode('hex')
>>> be='TWCTF{'
>>> en=c[:6]
>>> for i in range(251):
	for j in range(251):
		found=True
		for k in range(6):
			if (ord(be[k])*i+j)%251!=ord(en[k]):
				found=False
		if found:
			print i,j

			
156 76
>>> ans=''
>>> for ch in c:
	for i in range(256):
		if (i*156+76)%251==ord(ch):
			ans+=chr(i)
			break

		
>>> ans
'TWCTF{Faster_Than_Shinkansen!}'
>>> 
```
