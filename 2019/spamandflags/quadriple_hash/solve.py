from pwn import *

context.log_level='debug'

with open('res') as f:
    m0 = f.readline().strip()
    m1 = f.readline().strip()
assert m0 != m1
m0 += 'apple'
m1 += 'apple'
c = remote('35.231.4.77', 1337)
c.recvline()
c.recvline()
c.recvline()
c.sendline(m0)
c.sendline(m1)
c.interactive()
# SaF{h3y_sMAlL_inNEr_sT4Te_i5_w0rSE_w1th_enCRYpt1On}
