## Pwn

### babyheap
题目在初始时对堆的topchunk进行了随机化，并且使用calloc申请内存，会把已申请的内存块清空。

- 输入的时候又一个off by one漏洞，可以修改下一个chunk的size位，伪造heap chunk进行unlink。 
- 通过切分unsortbin的堆块将arena的地址写到一个可打印的chunk上。
- 修改fastbin的fd指针修改malloc hook为gadget地址。  
- 这时如果直接malloc，所有的gadget都不能用。另外一种办法：触发堆分配的error，在libc_error_msg的函数里会调用strdup函数，触发malloc，跳到gadget上面。

### RNote3
在 dele时没有对ptr进行初始化，如果先show A，delete的时候，输入的title没有在table中找到，此时ptr会是栈上的残留地址A，进而实现double free。

### RNote4
题目没有任何输出信息，edit的使用可以任意写堆地址，进而修改另外一个note的content指针实现任意地址写。   
题目原意想让使用dl fix up操作，下面是一个非预期解  

- alarm在libc里的地址和execve地址相近，如果修改alarm got表的低地址，有1/16的概率改为execve的地址。
- 这样修改free got表的地址，控制一下execve的参数，跳到alarm上面去。 

### simulator
一个mips指令模拟器，在写内存时没有对地址的下界进行检查，把v4改为负数，可以实现任意地址写。 

```c
int __cdecl write_to_real_mem(int a1, int a2, void *data_add)
{
  int v4; // [esp+Ch] [ebp-Ch]

  v4 = regs[2 * a2];
  if ( v4 > 1024 )
  {
    puts("memory access error");
    exit(0);
  }
  *((_DWORD *)data_add + 2 * v4 + 1) = regs[2 * a1];
  return pc++ + 1;
}
```
把stack check fail的got地址改掉，在程序退出的时候又一个明显的栈溢出。  

### stringer
一个很明显的double free，但是使用calloc申请内存，会把已申请的块清零，不知道怎么下手，很伤心。  

比赛结束才知道calloc如果申请的mmaped堆块，就不会清零。。。。。

```c
/* Two optional cases in which clearing not necessary */
if (chunk_is_mmapped (p))
{
  if (__builtin_expect (perturb_byte, 0))
    return memset (mem, 0, sz);
  return mem;
}
```

## Reverse
### babyre
题目对输入做了一个变换，然后输出要求和给出的结果一样。  
输入变换的逻辑在0x0804868B的函数，参数是每次输入的字符和一个long型数字0x1d082c23a72be4c1。  
变换的逻辑懒的逆了，直接把函数dump出来，暴力枚举所有字符，拿到flag。  
### babyre2
题目对输入的字符串转成了一个long型数组，对于数组中每个数字i乘上一个已知的数字再对N取余，要求结果和已知的另外一个数字相等。  

```
i*x=y  (mod N)
i=y*(x') (mod N)
```
使用欧几里得算法取逆，就可以求出i

### simplevm
手写了一个反汇编器，后来发现逻辑很简单，手动逆opcode也行。。。

```python
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

```
### simple re
加了一些代码混淆和反调，程序运行后子进程回去调试父进程，真正的flag检查逻辑是写在子进程里面的，自己就逆了半天假的检查逻辑，发现得出的结果不对。  
