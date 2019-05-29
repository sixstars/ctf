#coding=utf-8
from pwn import *
context.log_level="debug"
r=remote("49.4.26.104", 30027)
r.recvuntil('wait...\n')
elffile =  r.recvline()

with open("y.bin",'w') as f:
  f.write(elffile)
  f.close()


def read_until(fd, max_sz, end_ch = None):
    data = ''
    while len(data) < max_sz:
        try:
            tch = fd.read(1)
        except Exception, e:
            break  

        if end_ch != None and tch == end_ch:
            break

        if tch == '':
            break      
        data += tch
        #print data
    return data

def exec_serv(name,out):
    p = subprocess.Popen(name, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.stdin.write(out)
    return read_until(p.stdout, 0x100,'\n')

os.system("base64 -d y.bin | gunzip > /tmp/elf")
data = exec_serv("python fck.py /tmp/elf","")
r.sendline(data)
r.interactive()



