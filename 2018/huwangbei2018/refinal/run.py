with open("./code","r") as f:
    code=f.read()

def get_h_l(x):
    return ord(x)>>4,ord(x)&0xf

def ret(pc):
    f="%x: return"%pc
    pc+=1
    return f,pc

def jmp_if_buf4_p1(pc):
    target=ord(code[pc+1])+2+pc
    f="%x: jmp %x if buf[4] == -1"%(pc,target)
    pc+=2
    return f,pc

def jmp_if_buf4_1(pc):
    target=ord(code[pc+1])+2+pc
    f="%x: jmp %x if buf[4] == 1"%(pc,target)
    pc+=2
    return f,pc

def jmp_if_buf4_0(pc):
    target=ord(code[pc+1])+2+pc
    f="%x: jmp %x if buf[4] == 0"%(pc,target)
    pc+=2
    return f,pc

def xor_h_from_l(pc):
    h,l=get_h_l(code[pc+1])
    f = "%x: xor buf[%d],buf[%d]"%(pc,h,l)
    pc+=2
    return f,pc

def cmp(pc):
    h,l=get_h_l(code[pc+1])
    f = "%x: cmp buf[%d],buf[%d]"%(pc,h,l)
    pc+=2
    return f,pc
def pop_to_hidx(pc):
    h,l=get_h_l(code[pc+1])
    f="%x: pop buf[%d]"%(pc,h)
    pc+=2
    return f,pc

def push_num(pc):
    x=code[pc+1:pc+5]
    x=int(x.encode("hex"),16)
    f= "%x: push 0x%x"%(pc,x)
    pc+=5
    return f,pc

def loop_back(pc):
    target=pc-ord(code[pc+1])
    f="%x: goto %x until buf[3] == 0"%(pc,target)
    pc+=2
    return f,pc

def set_hidx_from_mem(pc):
    h,_=get_h_l(code[pc+1])
    f="%x: mov buf[%d],[m1]"%(pc,h)
    pc+=2
    return f,pc

def m1plusplus(pc):
    f="%x: add m1,1"%(pc)
    pc+=1
    return f,pc

def addadd_hidx(pc):
    h,_=get_h_l(code[pc+1])
    f="%x: add buf[%d],1"%(pc,h)
    pc+=2
    return f,pc

def add_to_h_from_l(pc):
    h,l=get_h_l(code[pc+1])
    f="%x: add buf[%d],buf[%d]"%(pc,h,l)
    pc+=2
    return f,pc

def m1subsub(pc):
    f="%x: sub m1,1"%pc
    pc+=1
    return f,pc

def mul_h_from_l(pc):
    h,l=get_h_l(code[pc+1])
    f="%x: mul buf[%d],buf[%d]"%(pc,h,l)
    pc+=2
    return f,pc
def Sub_h_from_l(pc):
    h,l=get_h_l(code[pc+1])
    f="%x: sub buf[%d],buf[%d]"%(pc,h,l)
    pc+=2
    return f,pc
vtable={
'C':ret,
'D':jmp_if_buf4_p1,
'E':None,
'F':set_hidx_from_mem,
'G':xor_h_from_l,
'H':cmp,
'I':m1plusplus,
'J':None,
'K':jmp_if_buf4_0,
'L':None,
'M':jmp_if_buf4_1,
'N':None,
'O':push_num,
'P':addadd_hidx,
'Q':None,
'R':None,
'S':add_to_h_from_l,
'T':pop_to_hidx,
'U':loop_back,
'V':m1subsub,
'W':None,
'X':mul_h_from_l,
'Y':Sub_h_from_l
}

pc=0
while pc < len(code):
    f,pc = vtable[code[pc]](pc)
    print f

