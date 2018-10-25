from Crypto.Cipher import AES

from pwn import *

context.log_level='debug'

c = remote('52.194.203.194', 21700)


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

k = '$#@!zxcvasdfqwer'
show(0)
ct = c.recvline().strip().decode('hex')
add(2, 1, 15, 'a'*15)
show(2)
ct2 = c.recvline().strip().decode('hex')
a = AES.new(key=k, IV='\x00'*16, mode=AES.MODE_CBC)
pt2 = a.decrypt(ct2)
pt = 'a'*15+'\x01'
iv = ''
for i in range(16):
    iv += chr(ord(pt[i])^ord(pt2[i]))
a = AES.new(key=k, IV=iv, mode=AES.MODE_CBC)
print a.decrypt(ct)

# flag:hitcon{*?!@_funny_c3ypt0_4nd_pwN__$$%#}
