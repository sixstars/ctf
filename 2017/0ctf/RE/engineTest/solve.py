from pwn import *
import z3

s=z3.Solver()
val = {}
val[0]=z3.Bool('c0')
val[1]=z3.Bool('c1')
s.add(val[0]==False)
s.add(val[1]==True)
for i in range(0x110):
    val[i+2] = z3.Bool('i_%d'%i)

f=open('cp','rb')
l1=u64(f.read(8))
l2=u64(f.read(8))
ops = []
for i in range(l2):
    ops.append(f.read(40))
#print ops[-1]
f.close()
f=open('opindex','rb') # memory dumped using gdb
for i in range(l2):
    ind=u64(f.read(8))
    t=ops[ind]
    opi=u64(t[:8])
    a1=u64(t[8:16])
    a2=u64(t[16:24])
    a3=u64(t[24:32])
    o1=u64(t[32:])
    if (opi==1):
        #cmd='Bit%di = Bit%di & Bit%di' % (o1,a1,a2)
        val[o1]=z3.And(val[a1],val[a2])
    elif (opi==2):
        #cmd='Bit%di = Bit%di | Bit%di' % (o1,a1,a2)
        val[o1]=z3.Or(val[a1],val[a2])
    elif (opi==3):
        #cmd='Bit%di = Bit%di!=Bit%di' % (o1,a1,a2)
        val[o1]=(val[a1]!=val[a2])
    elif (opi==4):
        #cmd='Bit%di = Bit%di if Bit%di else Bit%di' % (o1,a3,a1,a2)
        val[o1]=z3.If(val[a1],val[a2],val[a3])
    else:
        print 'Error op', opi
    #cmd=cmd.replace('Bit0i','0').replace('Bit1i','1')
    #print cmd
#print val[34792]
s.add(val[34792]==True)
print s.check()
m=s.model()
ans=[]
for i in range(0x110):
    ans.append(m[val[i+2]])
print ans
#flag{wind*w(s)_*f_B1ll(ion)_g@t5s}
