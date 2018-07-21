from pwn import *

context.log_level='error'

def once(d):
    c = remote('dogestore.ctfcompetition.com', 1337)
    c.send(d)
    res=c.recv()
    c.close()
    return res

with open('encrypted_secret','rb') as f:
    ct=f.read()
ct = map(ord,ct)
rle = [-1]*55
rsz = [-1]*55
for i in range(len(ct)/2-1):
    for j in range(128):
        print i,j
        '''
        if j!=0:
            ct[2*i+2]^=j
            tar2=once(''.join(map(chr,ct)))
            ct[2*i+2]^=j
        else:
            tar2='ga'
        '''
        ct[2*i]^=j
        tar=once(''.join(map(chr,ct)))
        '''
        if tar==tar2:
            rle[i]=j
            rsz[i]=0
        '''
        for k in range(1,5)[::-1]:
            if rle[i]!=-1:
                break
            ct[2*i+1]^=k
            ct[2*i+3]^=k
            res=once(''.join(map(chr,ct)))
            ct[2*i+1]^=k
            ct[2*i+3]^=k
            if res==tar:
                rle[i] = j
                rsz[i] = k
        ct[2*i]^=j
        if rle[i]!=-1:
            break
    print 'cur:'
    print rle
    print rsz
    exit()
print rel    
