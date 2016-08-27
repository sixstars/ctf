容易发现里面有段很像快速幂，仔细看下是在置换群上的幂操作，用户输入被当作little-endian的次数，所以就是置换群下的对数问题了

google一下第一个结果就是<http://echochamber.me/viewtopic.php?t=111164>

然后照着实现下就是了，代码如下
```
from struct import unpack

def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
 
    for n_i, a_i in zip(n, a):
        p = prod / n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod

def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a / b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

f=open('p.txt')
s=f.read()
p=[]
for i in range(len(s)/8):
    a=s[i*8:i*8+8].decode('hex')
    p.append(unpack('I',a)[0])

f=open('t.txt')
s=f.read()
t=[]
for i in range(len(s)/8):
    a=s[i*8:i*8+8].decode('hex')
    t.append(unpack('I',a)[0])

NUM=0x4000
assert len(p)==NUM
v=[0]*NUM
cycles=[]
for i in range(NUM):
    cycle=[]
    node=i
    while v[node]==0:
        v[node]=1
        cycle.append(node)
        node=p[node]
    if len(cycle)!=0:
        cycles.append(cycle)
v=[0]*NUM
tcycles=[]
for i in range(NUM):
    cycle=[]
    node=i
    while v[node]==0:
        v[node]=1
        cycle.append(node)
        node=t[node]
    if len(cycle)!=0:
        tcycles.append(cycle)

assert len(cycles)==len(tcycles) # happened to be true in these binary
aa=[]
nn=[]
for i in range(len(cycles)):
    assert cycles[i][0]==tcycles[i][0]
    if len(cycles[i])==1:
        continue
    tt=tcycles[i][1]
    r=cycles[i].index(tt)
    aa.append(r)
    nn.append(len(cycles[i]))
print nn
print aa
#print chinese_remainder(nn,aa)
```
直接跑会报错就把中国剩余定理部分扔个sage了，注意下endian的问题得到结果`03acc61fd6819a6eb4bbd311c5e72818`
