from twisted.internet import reactor, protocol
from Crypto.Cipher import AES
import os
import random
from secret import KEY,KEYSIZE,IV,FLAG

PORT = 6666

def pad(instr, length):
        if(length == None):
                print "Supply a length to pad to"
        elif(len(instr) % length == 0):
                print "No Padding Needed"
                return instr
        else:
                return instr + '\x04' * (length - (len(instr) % length ))

def encrypt_block(key, plaintext):
        encobj = AES.new(key, AES.MODE_ECB)
        return encobj.encrypt(plaintext).encode('hex')

def decrypt_block(key, ctxt):
        decobj = AES.new(key, AES.MODE_ECB)
        return decobj.decrypt(ctxt).encode('hex')

def xor_block(first,second):
        if(len(first) != len(second)):
                print "Blocks need to be the same length!"
                return -1

        first = list(first)
        second = list(second)
        for i in range(0,len(first)):
                first[i] = chr(ord(first[i]) ^ ord(second[i]))
        return ''.join(first)

def encrypt_cbc(key,IV, plaintext):
        if(len(plaintext) % len(key) != 0):
                plaintext = pad(plaintext,len(key))
        blocks = [plaintext[x:x+len(key)] for x in range(0,len(plaintext),len(key))]
        for i in range(0,len(blocks)):
                if (i == 0):
                        ctxt = xor_block(blocks[i],IV)
                        ctxt = encrypt_block(key,ctxt)
                else:
                        tmp = xor_block(blocks[i],ctxt[-1 * (len(key) * 2):].decode('hex')) 
                        ctxt = ctxt + encrypt_block(key,tmp)
        return ctxt

def decrypt_cbc(key,IV,ctxt):
        ctxt = ctxt.decode('hex')
        if(len(ctxt) % len(key) != 0):
                print "Invalid Key."
                return -1
        blocks = [ctxt[x:x+len(key)] for x in range(0,len(ctxt),len(key))]
        for i in range(0,len(blocks)):
                #print blocks[0].encode('hex')
                if (i == 0):
                        ptxt = decrypt_block(key,blocks[i])
                        ptxt = xor_block(ptxt.decode('hex'),IV)
                        #print ptxt.encode('hex')
                else:
                        tmp = decrypt_block(key,blocks[i])
                        tmp = xor_block(tmp.decode('hex'),blocks[i-1])
                        ptxt = ptxt + tmp
        return ptxt


def mkprofile(email):
	if((";" in email)):
		return -1
	prefix = "comment1=wowsuch%20CBC;userdata="
	suffix = ";coment2=%20suchsafe%20very%20encryptwowww"
	
	ptxt = prefix + email + suffix
	print ptxt
	return encrypt_cbc(KEY,IV,ptxt)	


def parse_profile(data):
	print "DATA:"
	print data	
	ptxt = decrypt_cbc(KEY,IV,data.encode('hex'))
	ptxt = ptxt.replace("\x04","")
	print ptxt
	if ";admin=true" in ptxt:
		return 1
	return 0


class MyServer(protocol.Protocol):
    def dataReceived(self,data):
	if(len(data) > 512):
		self.transport.write("Data too long.\n")
		self.transport.loseConnection()
		return

	if(data.startswith("mkprof:")):
		data = data[7:]
		resp = mkprofile(data)
		if (resp == -1):
			self.transport.write("No Cheating!\n")
		else:
			self.transport.write(resp + '\n')
	elif(data.startswith("parse:")):
		self.transport.write("Parsing Profile...")
		data = data[6:].decode('hex')
		if (len(data) % KEYSIZE != 0):
			self.transport.write("Invalid Ciphertext <length>\n")
			self.transport.loseConnection()
			return
		
		if(parse_profile(data) == 1):
			self.transport.write("Congratulations!\nThe FLAG is: ")
			self.transport.write(FLAG)
			self.transport.loseConnection()
		
		else:
			self.transport.write("You are a normal user.\n")
	
	else:
		self.transport.write("Syntax Error")
		self.transport.loseConnection()


class MyServerFactory(protocol.Factory):
    protocol = MyServer



factory = MyServerFactory()
reactor.listenTCP(PORT, factory)
reactor.run()
