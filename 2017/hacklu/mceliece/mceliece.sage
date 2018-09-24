#https://eprint.iacr.org/2009/452.pdf
DEBUG=0

F=GF(2^8)
z8=F.gen()

'''
n,k=4,2
cmsg=vector(F,[z8^7 + z8^4 + z8^3 + z8^2 + z8, z8^3 + 1, z8^7 + z8^5 + z8^3 + z8^2 + z8, z8^7 + z8^6 + z8^5 + z8^4 + z8^3 + z8^2 + 1])
gp=Matrix(F,k,n,[z8^2, 0, z8^3 + z8^2, z8^4 + z8^2, z8 + 1, 1, z8^2 + z8 + 1, z8^3 + z8 + 1])
'''

'''
n,k=6,3
cmsg=vector(F,[z8^7 + z8^6 + z8^2 + z8, z8^6 + z8^3 + z8^2, z8^7 + z8^4 + z8 + 1, 1, z8^7 + z8^6 + z8^5 + z8^4 + z8^3 + z8^2, z8^5 + z8^3 + z8^2])
gp=Matrix(F,k,n,[z8^2, z8^2, z8^4 + z8^3 + z8^2, z8^6 + z8^4 + z8^2, z8^5 + z8^4 + z8^3 + 1, z8^5 + z8^4, z8, 0, z8^4 + z8^3 + z8^2 + z8, z8^6 + z8^4 + z8^3 + z8, z8^5 + z8^3 + z8^2 + z8 + 1, z8^4 + z8^2 + z8, z8^4, z8^7 + z8^4 + z8^3 + z8, z8^5 + z8^4 + z8^3 + z8^2 + z8, z8^7 + z8^6 + z8^4, z8^7 + z8^6 + z8^2 + z8 + 1, z8^7 + z8^4 + z8^2 + z8])

n,k=6,3
cmsg=vector(F,[z8^6 + z8^3 + z8^2 + z8, z8^7 + z8^6 + z8^5 + z8^3 + z8^2, z8^4, z8^7 + z8^6 + z8^5 + z8^4 + z8^3 + z8^2 + z8 + 1, z8^4 + z8^3 + z8 + 1, z8^7 + z8^6 + z8^5 + z8^2])
gp=Matrix(F,k,n,[z8^2, z8^7 + z8^6 + z8^5, z8^5 + z8^3 + 1, z8^7 + z8^6 + z8^4 + 1, z8^6 + z8^3 + z8, z8^6 + z8^5 + z8 + 1, 0, z8^7 + z8^6 + z8^5 + z8^4, z8^7 + z8^6 + z8^3 + 1, z8^4 + z8^3 + z8^2 + z8, z8^7 + z8 + 1, z8^7 + z8^5 + z8^4 + 1, z8^7 + z8^4 + z8^3 + z8, z8^7 + z8^6 + z8^5 + z8^3 + z8^2 + 1, z8^7 + 1, z8^5 + z8^4 + z8 + 1, z8^7 + z8^5 + z8^2 + 1, z8^7 + z8^6 + z8^5 + z8^4 + z8^3 + z8^2])
'''


n,k=128,64
cmsg=load("ciphertext.sobj")
gp=load("publickey.sobj")

gpe=gp.echelon_form()

for ratio in F.list()[1:]:
    a=[0]*n
    a[1]=1
    succ=True
    for i in range(k,n):
        tar=gpe[0][i]/gpe[1][i]
        tar=tar/ratio
        res=0
        for x in F.list():
            if x!=0 and (x-a[1])/(x-a[0])==tar:
                if res!=0:
                    succ=False
                    break
                res=x
        if res==0:
            succ=False
        if not succ:
            break
        a[i]=res
    if not succ:
        continue
    for i in range(2,k):
        v0=gpe[0][k]/gpe[i][k]*(a[k]-a[0])
        v1=gpe[0][k+1]/gpe[i][k+1]*(a[k+1]-a[0])
        res=0
        for r2 in F.list()[1:]:
            for x in F.list()[1:]:
                if r2*(a[k]-x)==v0 and r2*(a[k+1]-x)==v1:
                    res=x
                    break
            if res!=0:
                break
        if res==0:
            succ=False
        if not succ:
            break
        a[i]=res
    if not succ:
        continue

    if DEBUG:
        print ratio
        print a

    mp=gp.matrix_from_rows_and_columns(range(k),range(k+1))
    cp=mp.right_kernel().basis()[-1]
    Ct = codes.GeneralizedReedSolomonCode(a[:k+1], k, cp)
    Et = codes.encoders.GRSEvaluationVectorEncoder(Ct)
    gm=Et.generator_matrix()
    co=gm.right_kernel().basis()[-1]
    Ct = codes.GeneralizedReedSolomonCode(a[:k+1], k, co)
    Et = codes.encoders.GRSEvaluationVectorEncoder(Ct)
    gtmp1=Et.generator_matrix()
    gtmp2=gtmp1.matrix_from_rows_and_columns(range(k),range(k))
    mtmp2=gp.matrix_from_rows_and_columns(range(k),range(k))
    h=mtmp2*gtmp2.inverse()
    g=h.inverse()*gp
    cols=g[0]

    if DEBUG:
        print cols
        
    try:
        C = codes.GeneralizedReedSolomonCode(a, k, cols)
        E = codes.encoders.GRSEvaluationVectorEncoder(C)
        D = codes.decoders.GRSBerlekampWelchDecoder(C)
        g=E.generator_matrix()
        tmp=D.decode_to_message(cmsg)
        msg=vector(tmp)*h.inverse()
        print msg
    except Exception,ee:
        continue
