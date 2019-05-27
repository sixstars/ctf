# can also solve babysampling

from hashlib import sha256
from itertools import product

with open('output','rb') as f:
    s=f.read()
tarh = "d67c35a8f45e9c36c9bdb0e73027a3f89aa3bdd940cc200d7f0655af7f0a8dba"

bs = ''.join(map(lambda x:bin(ord(x))[2:].rjust(8,'0'),s))
print len(bs)
#print bs

seq = []
F = GF(2)
for i in range(1024):
    seq.append(F(int(bs[i])))

P.<x> = PolynomialRing(F)
poly = berlekamp_massey(seq)
print poly
'''
v = vector(poly)
print int(''.join(map(str,v[:-1])),2)
'''

p7 = poly.subs(x^7)
fs = factor(p7)
#tar = 559282078126269518888830963030439834975
#tar = 404314640861877153229506089020527528203
tar=658830303166448434138558730570919555209

tmp = [0]*128
mat = [vector(GF(2),tmp)]
for i in range(128):
    tmp = [0]*128
    tmp[i] = 1
    mat.append(vector(GF(2),tmp))

def solveone(msk):
    v = map(int, bin(msk)[2:])
    if len(v)<129:
        pre = [0]*(129-len(v))
        v = pre+v
    assert len(v)==129
    mata = deepcopy(mat)
    for i in range(129, 129+7*128+1):
        tmp = [0]*128
        tmp = vector(GF(2),tmp)
        for j in range(129):
            if v[j]==1:
                tmp += mata[i-129+j]
        mata.append(tmp)
    equs = []
    res = []

    for i in range(128):
        res.append(seq[i])
        equs.append(mata[129+7*i])
    #equs = matrix(GF(2),equs)
    #res = vector(GF(2),res)

    freedom = 128-matrix(GF(2),equs).rank()
    print freedom
    if freedom>6:
        return

    for xs in product(range(2),repeat=freedom):
        equsa = deepcopy(equs)
        resa = deepcopy(res)
        for ix in range(freedom):
            equsa.append(mat[ix+1])
            resa.append(xs[ix])
        equsa = matrix(GF(2),equsa)
        resa = vector(GF(2),resa)
        try:
            X = equsa.solve_right(resa)
        except:
            continue
        assert len(X)==128
        val = int(''.join(map(str,X)),2)
        h = hex(val)[2:].strip('L').rjust(32,'0')
        flag = 'flag{'+h+'}'
        print flag
        if sha256(flag).hexdigest()==tarh:
            print '!!!!!!!!!!!!!!!!!!!!!!!'
            print flag
            exit()
        

def do_search(pos,cur):
    if pos>=len(fs):
        if cur.degree()==129:
            #print cur
            msk = int(''.join(map(str,vector(cur)[:-1])),2)
            print 'trying',msk
            solveone(msk)
        return
    if cur.degree()>129:
        return
    for i in range(fs[pos][1]+1):
        do_search(pos+1, cur*fs[pos][0]^i)
    
do_search(0, x^0)

#solveone(tar)

'''
around 2h
trying 346197146495438806320168129056019518903

'''
