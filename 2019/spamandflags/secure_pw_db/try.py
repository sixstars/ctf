import random

p=0xffffffff00000001000000000000000000000000ffffffffffffffffffffffffL

def dopow(x,n):
    bits = bin(n)[2:]
    r = 0
    for b in bits:
        r = -2*r
        if r==0:
            a=x
        else:
            a = -(r+x)
        if b=='1':
            r=a
    return r

def dorev(x):
    op = []
    while x!=0 and x!=1:
        if x%2==1:
            op.append('a')
            x=-x-1
        else:
            op.append('m')
            x/=-2
    r=x
    op = op[::-1]
    for o in op:
        if o=='a':
            r+=1
        elif o=='m':
            r*=2
    return r

a = -85961949238027824736601398012677843206
ans = dorev(a)
print ans
print dopow(1,ans)
print dopow(1,0b1000001011011000110110101101111011100110111010000100000011101000110100001100101011100100110010100100000001110100010100100001010)
exit()
for _ in range(50):
    i = random.randint(0,p-1)
    t = dopow(1,i)
    print i,t
    ti = dorev(t)
    t2 = dopow(1,ti)
    assert t==t2
