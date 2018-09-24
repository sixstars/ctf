def Moni(a,n):
    p = a
    q = n
    x = 0
    y = 1
    z = int(q)/p
    while(1 != p):
        t = p
        p = q % p
        q = t
        t = y
        y = x - y*z
        x = t
        z = int(q)/p
    y=y%n
    if(y < 0):
        y += n
    return y

array1=[
    0x2b7192452905e8fb,0x7ba58f82bd898035,
    0xa3112746582e1434,0x163f756fcc221ab0,
    0xecc78e6fb9cba1fe,0xdcdd8b49ea5d7e14,
    0xa2845fe0b3096f8e,0xaaaaaaaaaa975d1c
]
array2=[
    0x20656d6f636c6557,
    0x2046544352206f74,
    0x6548202138313032,
    0x2061207369206572,
    0x6320455279626142,
    0x65676e656c6c6168,
    0x756f7920726f6620,
    0xffffffffffff002e,
    0xffffffffffffffff,
    0xffffffffffffffff,
    0xffffffffffffffff,
    0xffffffffffffffff,
    0xffffffffffffffff,
    0xffffffffffffffff,
    0xffffffffffffffff,
    0xffffffffffffffff
]

N=0xFFFFFFFFFFFFFFC5
ans=[]
for i in range(8):
    tmp=Moni(array2[i],N)
    ans.append(tmp*array1[i]%N)

def hex2str(i):
    return hex(i)[2:-1].decode("hex")[::-1]


print "".join(map(hex2str,ans))





