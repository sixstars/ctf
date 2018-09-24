#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *

class VM:
	def __init__(self,code,stdin):
		self.reg1=0
		self.reg2=0
		self.pc=0
		self.npc=0
		self.code=map(ord,list(code))
		self.stdin=stdin
		self.fp=0
		self.stdout=[]

	def getInt(self,begin):
		l="".join(map(chr,self.code[begin:begin+4]))
		return u32(l)

	def getByte(self,begin):
		return self.code[begin]

	def setInt(self,begin,value):
		self.setByte(begin,value&0xff)
		self.setByte(begin,(value&0xff00) > 8)
		self.setByte(begin,(value&0xff0000) >16)
		self.setByte(begin,(value&0xff000000) >24)
	
	def setByte(self,begin,value):
		self.code[begin]=value&0xff

	def getchr(self):
		v=self.stdin[self.fp]
		self.fp+=1
		return ord(v)

	def putchr(self,v):
		self.stdout.append(chr(v&0xff))

	def disasm(self):
		asm_code=[]
		try:
			while self.npc<len(self.code):
				self.npc=self.pc+1
				opcode=self.code[self.pc]
				if opcode==0:
					v1=self.getInt(self.npc)
					asm_code.append("%x:ret 0x%x"%(self.pc,v1))
					break
				elif opcode==1:
					self.npc=self.getInt(self.npc)
					asm_code.append("%x:jmp 0x%x#"%(self.pc,self.npc))
				elif opcode==2:
					self.npc=self.pc+9
					v1=self.getInt(self.pc+1)
					v2=self.getInt(self.pc+5)
					self.setInt(self.pc+1,v1*v2)
					asm_code.append("%x:code[0x%x]=code[0x%x]*code[0x%x]"%(self.pc,self.pc+1,v1,v2))
				elif opcode==3:
					self.npc+=4
					tmp=self.getInt(self.pc+1)
					self.reg1=self.getByte(tmp)
					asm_code.append("%x:mov reg1,byte code[0x%x]"%(self.pc,tmp))
				elif opcode==4:
					self.npc+=4
					tmp=self.getInt(self.pc+1)
					self.setByte(tmp,self.reg1)
					asm_code.append("%x:mov byte code[0x%x],reg1"%(self.pc,tmp))
				elif opcode==5:
					self.npc+=4
					tmp=self.getInt(self.pc+1)
					self.reg2=self.getByte(tmp)
					asm_code.append("%x:mov reg2,byte code[0x%x]"%(self.pc,tmp))
				elif opcode==6:
					self.npc+=4
					tmp=self.getInt(self.pc+1)
					self.setByte(tmp,self.reg2)
					asm_code.append("%x:mov byte code[0x%x],reg2 #0x%x"%(self.pc,tmp,self.reg2))
				elif opcode==7:
					self.reg1+=self.reg2
					asm_code.append("add reg1,reg2")
				elif opcode==8:
					self.reg1=(self.reg1&self.reg2)^0xffffffff
					asm_code.append("%x:not and reg1,reg2"%(self.pc))
				elif opcode==0xa:
					self.reg1=self.getchr()
					asm_code.append("%x:getchr %c to reg1"%(self.pc,chr(self.reg1&0xff)))
				elif opcode==0xb:
					self.putchr(self.reg1)
					asm_code.append("%x:putchr %c"%(self.pc,chr(self.reg1&0xff)))
				elif opcode==0xc:
					tmp=self.getInt(self.npc)
					v1=self.getByte(tmp)
					if v1!=0:
						self.npc=self.getInt(self.npc+4)
						self.setByte(tmp,v1-1)
						asm_code.append("%x:jmp to 0x%x because byte code[0x%x]!=0"%(self.pc,self.npc,tmp))
					else:
						self.npc+=8
						asm_code.append("%x:now jmp to 0x%x"%(self.pc,self.npc))
				elif opcode==0xd:
					self.reg1+=1
					asm_code.append("%x:reg1++"%self.pc)
				elif opcode==0xe:
					self.reg2+=1
					asm_code.append("%x:reg2++"%self.pc)
				elif opcode==0xf:
					self.reg1=self.reg2
					asm_code.append("%x:mov reg1,reg2"%(self.pc))
				elif opcode==0x10:
					self.reg2=self.reg1
					asm_code.append("%x:mov reg2,reg1"%(self.pc))
				elif opcode==0x11:
					tmp=self.getInt(self.npc)
					self.reg1+=tmp
					self.npc+=4
					asm_code.append("%0x:add reg1,0x%x# reg1=0x%x"%(self.pc,tmp,self.reg1))
				elif opcode==0x12:
					self.reg1=self.getByte(self.reg2)
					asm_code.append("%x:mov reg1,byte code[reg2(0x%x)] # 0x%x"%(self.pc,self.reg2,self.reg1))
				elif opcode==0x13:
					tmp=self.reg1
					self.reg1=self.getInt(tmp)&0xff
					asm_code.append("%x:mov reg1,byte code[reg1(0x%x)] # 0x%x"%(self.pc,tmp,self.reg1))
				elif opcode==0x14:
					self.reg1=self.getInt(self.npc)
					self.npc+=4
					asm_code.append("%x:mov reg1,0x%x"%(self.pc,self.reg1))
				elif opcode==0x15:
					self.reg2=self.getInt(self.npc)
					self.npc+=4
					asm_code.append("%x:mov reg2,0x%x"%(self.pc,self.reg2))
				elif opcode==0x16:
					self.setByte(self.reg2,self.reg1)
					asm_code.append("%x:code[0x%x]=reg1#0x%x"%(self.pc,self.reg2,self.reg1))
				elif opcode==0x17:
					self.reg1-=self.reg2
					asm_code.append("%x:sub reg1,reg2"%(self.pc))
				elif opcode==0x18:
					tmp=self.getInt(self.npc)
					asm_code.append("%x:jmp 0x%x if reg1==0 "%(self.pc,self.npc))
					if self.reg1!=0:
						self.npc=tmp
					else:
						self.npc+=4
				else:
					asm_code.append("%x:nop"%self.pc)
				self.pc=self.npc

		except Exception as e:
			print "\n".join(asm_code)
			print "pc:0x%x"%self.pc			
			raise e
		return "\n".join(asm_code)


def main():
	with open("p.bin","r") as f:
		code=f.read()
	vm=VM(code,"61f6".rjust(0x20,"a"))
	print vm.disasm()



if __name__ == '__main__':
	main()
		
