#encoding = utf-8
import random,sys,struct
import base64 as b64
import os
import hmac
from hashlib import sha512,sha1
from time import time
from pwn import *


def hash2int(*params): 
	sha=sha512()
	for el in params:
		sha.update("%r"%el)
	return int(sha.hexdigest(), 16)  
N = 1501763523645191865825715850305314918471290802252408144539280540647301821
'''
	def cryptrand(self,n=2048):  
		p1=self.hash2int(os.urandom(40))<<1600  
		p1+=self.hash2int(p1)<<1000
		p1+=self.hash2int(p1)<<500
		p1+=self.hash2int(p1)
		bitmask=((2<<(n+1))-1)
		p1=(p1&bitmask)
		return  (p1% self.N)
	def sendInt(self,toSend):
		s=hex(toSend)
		s=s[2:]
		if s[-1]=="L":
			s=s[:-1]
		self.request.sendall(s+"\n")
	def readInt(self):
		req=self.request
		leng = struct.unpack("H", req.recv(2))[0]
		if leng>520:
			req.sendall("Sorry that is too long a number\n")
			req.close()
			return None
		toRead = ""
		while len(toRead) < leng:
			toRead += req.recv(leng - len(toRead))
		if len(toRead) > leng:
			req.sendall("Something wrong!\n")
			req.close()
			return None
		return int(toRead,16)
		
	def checkBlacklist(self):
		foreign=self.request.getpeername()[0]
		if foreign in self.accepted:
			while(len(self.accepted[foreign]) >0 and
				self.accepted[foreign][0]<time()-600):
				del self.accepted[foreign][0]
			if len(self.accepted[foreign])>5:
				self.request.send("Too many requests too quick sorry\n")
				self.request.close()
				return False
		else:
			self.accepted[foreign]=[]
		return True

	def getParamsFromClient(self):
		N=self.N
		req=self.request
		index=self.readInt()
		if index is None:
			return
		if index<2 or index>N/2:
    #brute force attempt
			req.sendall("A Wrong move against the motherland!\n")
			req.close()
			return None
		req.sendall("Please provide your temporary key, be careful!\n")
		ckey=self.readInt()
		if ckey is None:
			return None
		if  ckey%N==0:
			req.sendall("Wrong way to xidian\n")
			req.close()
			return None
		return ckey,index


	def doCryptAttack(self,index,ckey,salt):
		N=self.N

		password = ""
		hash2int= self.hash2int
		salt=hash2int(index)

		storedKey = pow(index, hash2int(salt, password), N)
		coefSlush = 3
		
		skeyPriv = self.cryptrand()
		skey = (coefSlush * storedKey + 
			pow(index, skeyPriv, N)) % N
		
		self.sendInt(salt)
		print 'salt',salt
		print '\n'
		self.sendInt(skey)
		print 'sKey',skey
		
		slush = hash2int(ckey, skey)
		tempAgreedKey = hash2int(pow(ckey * pow(storedKey, slush, N), skeyPriv, N))
		return tempAgreedKey,skey

	def handle(self):
		N=self.N
		hash2int=self.hash2int
		req = self.request
		req.sendall("Welcome to 2015 xidian ctf's checkin server, please provide 2 magic numbers!\n")

		ckey,index=self.getParamsFromClient()
		print ckey
		print '\n'
		print index

		salt=self.hash2int(index)
		tempAgreedKey,skey=self.doCryptAttack(index,ckey,salt)
		print 'akey',tempAgreedKey


		finalKey=hash2int(hash2int(N) ^ hash2int(index), hash2int(index), salt, 
			ckey, skey, tempAgreedKey)

		print 'genkey',finalKey

		check=self.readInt()

		if(check==finalKey):
			req.sendall("Well done com rade, the flag is XDCTF{xxxxxx} .\n")

		req.close()
'''

def doSend(num):
	s=hex(num)
	return struct.pack('H',len(s))+s


if __name__ == "__main__":
	context.log_level='debug'
	#conn = remote("127.0.0.1",5000)
	conn = remote("133.130.52.128",5000)
	conn.recv()
	index=53538541699666989075104314189461622667506313026452523318908741414211402
	prob=[]
	for i in range(5):
		prob.append(hash2int(pow(index,i,N)))
	print prob
	ckey=1
	print doSend(index)
	print hash2int(index)
	conn.send(doSend(index))
	conn.recv()
	conn.send(doSend(ckey))
	r=conn.recv()
	salt=int(r,16)
	r=conn.recv()
	skey=int(r,16)
	slush = hash2int(ckey, skey)
	tempAgreedKey = prob[0]
	finalKey=hash2int(hash2int(N) ^ hash2int(index), hash2int(index), salt, ckey, skey, tempAgreedKey)
	conn.send(doSend(finalKey))
	r=conn.recv()
	if "flag" in r:
		print "-----------------"
		print r
		print "-----------------"
	conn.recv()
