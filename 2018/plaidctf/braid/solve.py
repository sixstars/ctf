f=open('data.txt')
s=f.readline()
xx,yy = eval(s)
s=f.readline()
cc,enc = eval(s)

N=140

'''
def gen(f):
    res = []
    pos = range(N)
    for i in range(N):
        for j in range(N):
            if tmp[j]==i:
                it = f[j]
                while it>i:
                    it-=1
                    tmp=pos[it]
                    pos[it]=
                    res.append(it)
                break

fw=open('forsage.txt','w')
fw.write(str(x[0])+',')
for factor in x[1]:
    ss = gen(factor)
    fw.write(repr(ss)+'\n') # x[2] = 0
fw.write(str(y[0])+',')
for factor in y[1]:
    ss = gen(factor)
    fw.write(repr(ss)+'\n') # x[2] = 0
fw.write(str(c0[0])+',')
for factor in c0[1]:
    ss = gen(factor)
    fw.write(repr(ss)+'\n') # x[2] = 0
'''

from copy import copy, deepcopy
import random
from hashlib import sha256

class NotImplemented(Exception):
    pass

def xor(x,y):
    return "".join(chr(ord(a)^ord(b)) for a,b in zip(x,y))

def id_perm(N):
    return [i for i in range(N)]

def sort_perm(a, b, s, l, h):
    if l >= h:
        return

    u = id_perm(len(a))
    v = id_perm(len(a))
    w = id_perm(len(a))
    m = (l + h) / 2
    sort_perm(a, b, s, l, m)
    sort_perm(a, b, s, m + 1, h)

    u[m] = a[s[m]]
    v[m] = b[s[m]]
    if l < m:
        for i in reversed(range(l, m)):
            u[i] = min(a[s[i]], u[i+1])
            v[i] = min(b[s[i]], v[i+1])
    u[m+1] = a[s[m+1]]
    v[m+1] = b[s[m+1]]
    if h > m + 1:
        for i in range(m + 2, h+1):
            u[i] = max(a[s[i]], u[i - 1])
            v[i] = max(b[s[i]], v[i - 1])

    p = l
    q = m + 1
    for i in range(l, h+1):
        if p > m or (q <= h and u[p] > u[q] and v[p] > v[q]):
            w[i] = s[q]
            q += 1
        else:
            w[i] = s[p]
            p += 1
    for i in range(l, h+1):
        s[i] = w[i]

def rand():
    return random.randint(0, 2**32)

class Factor(object):
    def __init__(self, N, perm=None):
        self.N = N
        if perm is None:
            self.perm = id_perm(N)
        else:
            self.perm = perm

    @staticmethod
    def random(N):
        perm = id_perm(N)
        for i in range(N):
            j = i + rand() % (N - i)
            z = perm[i]
            perm[i] = perm[j]
            perm[j] = z
        return Factor(N, perm)

    @staticmethod
    def _delta_table(N, i, k):
        return N - i - 1 if (k & 1) else i

    @staticmethod
    def delta(N, k):
        D = Factor(N)
        for i in range(N):
            D.perm[i] = Factor._delta_table(N, i, k)
        return D

    def is_identity(self):
        return self.perm == id_perm(self.N)

    def right_multiply(self, b):
        for i in range(self.N):
            self.perm[i] = b.perm[self.perm[i]]

    def left_multiply(self, b):
        tmp = id_perm(self.N)
        for i in range(self.N):
            tmp[i] = self.perm[b.perm[i]]
        self.perm = tmp

    def flip(self, k):
        result = Factor(self.N)
        for i in range(self.N):
            d = Factor._delta_table
            result.perm[i] = d(self.N, self.perm[d(self.N, i, -k)], k)
        return result

    def left_meet(self, other):
        s = id_perm(self.N)
        a = copy(self.perm)
        b = copy(other.perm)
        sort_perm(a, b, s, 0, self.N-1)
        for i in range(self.N):
            self.perm[s[i]] = i

    def make_left_weighted(self, b):
        x = ~self * self.delta(1)
        x.left_meet(b)
        if x.is_identity():
            return False
        else:
            self.right_multiply(x)
            b.left_multiply(~x)
            return True

    def expand(self, N, offset):
        assert N >= self.N + offset
        newperm = id_perm(N)
        for i in range(self.N):
            newperm[i + offset] = self.perm[i] + offset
        self.perm = newperm
        self.N = N

    def invert(self):
        tmp = copy(self.perm)
        for i in range(self.N):
            tmp[self.perm[i]] = i
        self.perm = tmp

    def __mul__(self, other):
        if isinstance(other, Factor):
            result = deepcopy(self)
            result.right_multiply(other)
            return result
        elif isinstance(other, Braid):
            result = deepcopy(other)
            result.left_multiply(self)
            return result
        else:
            raise NotImplemented


    def __rmul__(self, other):
        result = deepcopy(self)
        result.left_multiply(other)
        return result

    def __invert__(self):
        result = deepcopy(self)
        result.invert()
        return result

    def __eq__(self, other):
        return self.perm == other.perm

    def __repr__(self):
        return repr(self.perm)

    __str__ = __repr__

class Braid(object):
    def __init__(self, N):
        self.N = N
        self.left_delta = 0
        self.right_delta = 0
        self.factors = []

    @staticmethod
    def random(N, length):
        res = Braid(N)
        for i in range(length):
            f = Factor.random(N)
            res *= f
        return res

    def left_multiply(self, other):
        if isinstance(other, Braid):
            self.left_delta += other.right_delta
            for f in reversed(other.factors):
                self.left_multiply(f)
            self.left_delta += other.left_delta
        elif isinstance(other, Factor):
            self.factors.insert(0, other.flip(self.left_delta))
        else:
            raise NotImplemented

    def right_multiply(self, other):
        if isinstance(other, Braid):
            self.right_delta += other.left_delta
            for f in other.factors:
                self.right_multiply(f)
            self.right_delta += other.right_delta
        elif isinstance(other, Factor):
            self.factors.append(other.flip(-self.right_delta))
        else:
            raise NotImplemented

    def to_normal_form(self):
        if self.right_delta != 0:
            self.factors = map(lambda f: f.flip(self.right_delta), self.factors)
            self.left_delta += self.right_delta
            self.right_delta = 0

        D = Factor.delta(self.N, 1)
        A = self.factors
        l = len(A) - 1
        for i in reversed(range(l+1)):
            for j in range(i, l):
                B = (~A[j]) * D
                B.left_meet(A[j+1])
                if B.is_identity():
                    break
                A[j].right_multiply(B)
                A[j+1].left_multiply(~B)

        while len(self.factors) > 0 and self.factors[0] == D:
            self.factors.pop(0)
            self.left_delta += 1

        while len(self.factors) > 0 and self.factors[-1].is_identity():
            self.factors.pop(-1)

    def expand(self, N, offset):
        assert N >= self.N + offset
        for f in self.factors:
            f.expand(N, offset)
        self.N = N

    def __eq__(self, other):
        if self.left_delta != other.left_delta:
            return False
        if self.right_delta != other.right_delta:
            return False
        if self.factors != other.factors:
            return False
        return True

    def __mul__(self, other):
        result = deepcopy(self)
        result.right_multiply(other)
        return result

    def __invert__(self):
        result = Braid(self.N)
        result.left_delta = -self.right_delta
        result.right_delta = 0
        f = Factor(self.N)
        for fp in reversed(self.factors):
            for i in range(self.N):
                f.perm[fp.perm[i]] = Factor._delta_table(self.N, i, 1)
            result.factors.append(f.flip(-result.right_delta))
            result.right_delta -= 1
        result.right_delta -= self.left_delta
        return result

    def __repr__(self):
        return repr((self.left_delta, self.factors, self.right_delta))

    __str__ = __repr__


def cons(xx):
    x=Braid(N)
    for p in xx[1]:
        x.factors.append(Factor(N,perm=p))
    x.left_delta = xx[0]
    x.right_delta = xx[2]
    return x

x=cons(xx)
y=cons(yy)
c0=cons(cc)

def algoa(v,w):
    '''
    Algorithm A in https://link.springer.com/content/pdf/10.1007/3-540-36288-6_14.pdf
    '''
    # v,w already in normal form
    a = Braid(N)
    while w.left_delta < v.left_delta:
        r = w.left_delta
        w1 = Braid(N)
        w1.factors.append(w.factors[0])
        w1 = ~w1
        w1.left_delta += r
        w1.right_delta += -r
        
        ga = w1
        '''
        if r<0:
            tau = ~tau
            r=-r
        for i in range(r):
            ga = ga*tau
        '''
        #ga.left_delta += 1
        #print ga.left_delta, ga.right_delta
        a = ga*a
        #print w.left_delta,w.right_delta
        bak=w.left_delta
        w = ga * w * (~ga)
        w.to_normal_form()
        print w.left_delta,w.right_delta
        if bak>w.left_delta:
            exit()
    while len(w.factors) > len(v.factors):
        ga = Braid(N)
        ga.factors.append(w.factors[-1])
        a = ga*a
        a.to_normal_form()
        w = ga * w * (~ga)
        w.to_normal_form()
    #print 'v',v
    #print 'w',w

    '''
    https://pdfs.semanticscholar.org/b4ea/35f8c157d3799c2dae05d7a0d46def815818.pdf
    '''
    tar = []
    tar.append(deepcopy(w))
    cnt=0
    for ii in range(3):
        cnt+=1
        if cnt==30:
            break
        r = w.left_delta
        w1 = Braid(N)
        w1.factors.append(w.factors[0])
        w1 = ~w1
        w1.left_delta += r
        w1.right_delta += -r    
        ga = w1
        a = ga*a
        a.to_normal_form()
        w = ga * w * (~ga)
        w.to_normal_form()
        if cnt%20==0:
            print 'step:',cnt
        for i in reversed(range(len(tar))):
            if w==tar[i]:
                print '!!!!!!!!!!!!!!!!!!!!!!'
                print cnt,i
                break
        if w==v:
            print 'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGG'
            exit()
        tar.append(deepcopy(w))

    a2 = Braid(N)
    tar2 = []
    tar2.append(deepcopy(v))
    cnt=0
    for ii in range(3):
        cnt+=1
        if cnt==30:
            break
        r = v.left_delta
        w1 = Braid(N)
        w1.factors.append(v.factors[0])
        w1 = ~w1
        w1.left_delta += r
        w1.right_delta += -r
        a2 = w1*a2
        a2.to_normal_form()
        v = w1 * v * (~w1)
        v.to_normal_form()
        if cnt%20==0:
            print 'step:',cnt
        for i in reversed(range(len(tar2))):
            if v==tar2[i]:
                print '!!!!!!!!!!!!!!!!!!!!!!'
                print cnt,i
                break
        tar2.append(deepcopy(v))
    if v==w:
        print '6666666666666'
        return a,a2
    '''
    for i in reversed(range(len(tar))):
        if tar2[-1] == tar[i]:
            print 'GGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG'
            print len(tar2)-1,i
    '''
    '''
    mu = Braid(N)
    mu.factors.append(Factor(N, perm= guess(v,w)))
    a = mu*a
    w = mu * w * (~mu)
    w.to_normal_form()
    #print 'a',a
    #print 'wf',w
    if v==w:
        a.to_normal_form()
        return a
    else:
        print 'wtf'
        exit()
    '''

def getperm(v):
    N = len(v.factors[0].perm)
    pv = range(N)
    for f in v.factors:
        for i in range(N):
            pv[i] = f.perm[pv[i]]
    return pv

def guess(v,w):
    #print v,w
    pv = getperm(v)
    pw = getperm(w)
    print pv,pw
    tau = range(N)
    v = [0]*N
    for i in reversed(range(N)):
        r=i
        s=i
        while v[r]==0:
            v[r]=1
            r=pv[r]
            s=pw[s]
            if r!=s:
                tau[r]=s
    v = [0]*N
    for i in reversed(range(N)):
        if v[i]==0:
            v[i]=1
            r=i
            while v[tau[r]]==0:
                r=tau[r]
                v[r]=1
            tau[r]=i
    ans = [0]*N
    for i in range(N):
        ans[tau[i]] = i

    ansv = perminv(ans)
    if pprod(pprod(ansv,pv),ans)!=pw:
        print 'gya!'
    print ans
    return ans
    #return [1,0,3,2]

def perminv(a):
    c = range(len(a))
    for i in range(len(a)):
        c[a[i]]=i
    return c

def pprod(a,b):
    c=copy(a)
    for i in range(len(a)):
        c[i]=b[c[i]]
    return c

'''
pv=[3,2,1,4,0]
pa=[2,0,1,3,4]
pai=perminv(pa)
pw=pprod(pprod(pai,pv),pa)
exit()
'''
'''
N=4
L=2

x = Braid.random(N, L)
x.to_normal_form()
a = Braid.random(N/2, L)
a.expand(N, N/2)
y = a * x * (~a)
y.to_normal_form()

fw=open('testdata.txt','w')
print >>fw, (x,y)
print >>fw, a

fw=open('testdata2.txt')
s=fw.readline()
xx,yy = eval(s)
s=fw.readline()
aa = eval(s)
x=cons(xx)
y=cons(yy)
a=cons(aa)
'''
'''
b = algoa(x,y)
print b
sth = b * x * (~b)
sth.to_normal_form()
assert sth==y
print 'ohhhhhh'
'''

t1,t2 = algoa(x,c0)

b = (~t1)*t2
r1 = b*x*(~b)
r1.to_normal_form()
if c0==r1:
    print 'wow'
else:
    print 'lol'
    exit()

c1 = b * y * (~b)
c1.to_normal_form()
flag = xor(sha256(str(c1)).digest(), enc.decode('hex'))
print flag
