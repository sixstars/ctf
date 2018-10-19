def num_to_list(num):
    num = int(num)
    l = []
    for i in range(385):
        l.append(num%int(2))
        num /= int(2)
    return l[::-1]


f = open('mat')
m1=f.readline()
m1=eval(m1)
m1=matrix(GF(2),m1)
m2=f.readline()
m2=eval(m2)
m2=matrix(GF(2),m2)

t1=num_to_list(0x1e33c7fca3a3e2e07597c77e9ceed9808916cbfdce246dd894421aecba76dd23dc04b4e5e28d78fa49f9f16ee2ff540d0)
t1=vector(GF(2),t1)
t2=num_to_list(0x1713d455b5e85a6d8e58a9c42e326f884eae066858245046a1a128d777d10990a9d8cecb8cc4f9b005cf301617ef28f3)
t2=vector(GF(2),t2)

mm=m1-m2
print mm.rank()
tt=t1-t2
xx=mm.solve_right(tt)
assert t1-m1*xx == t2-m2*xx
kk = t1-m1*xx

chal=num_to_list(0x1baa06181d1d5d01236eb4bd8dff9cf9976494f1c73bf333409f473cddeab93b5a2c1f2bd3659308ea56515664212c8c8)
chal=vector(GF(2),chal)
ans=chal+kk
print kk
print ans
