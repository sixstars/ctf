from pwn import *
import string
import itertools

context.log_level='debug'

def doinit(key):
	l=len(key)/6
	for i in range(l):
		keydic[key[i*6:(i+1)*6]]=i

def getdic(str):
	global keydic
	global key
	conn=remote("159.203.87.2",5678)
	conn.recvline()
	newkey=conn.recvline()
	conn.recvline()
	conn.send(str+'\n')
	res=conn.recv()
	res=res.strip()
	newkey=newkey.strip()
	if key=='':
		key=newkey
		doinit(key)
	if key!=newkey:
		key=newkey
		keydic={}
		doinit(key)
		print "key changed"
	l=len(str)/6
	for i in range(l):
		tmpblk=res[i*6:(i+1)*6]
		if keydic.get(tmpblk)!=None:
			ans[keydic[tmpblk]]=str[i*6:(i+1)*6]
			print keydic[tmpblk],ans[keydic[tmpblk]]

keydic={}
ans=[]
for i in range(78/6):
	ans.append('')
# test
'''
dic['101010']='313233'
dic['111111']='343536'
decrypt('101010111111101010')
exit()
'''
key=''
table=string.ascii_lowercase
sendstr=''
sendlen=0
for b0 in table:
	for b1 in table:
		for b2 in table:
			sendstr+=b0.encode('hex')+b1.encode('hex')+b2.encode('hex')
			sendlen+=6
			if sendlen==180:
				getdic(sendstr)				
				sendstr=''
				sendlen=0
				print ans
print ans
			
