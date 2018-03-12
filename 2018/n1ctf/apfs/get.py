#!/usr/bin/env python
# coding:utf-8

import commands

for i in xrange(531):
    cmd = './t /Volumes/N1CTF_APFS/ctf/{:04d}.txt'.format(i)
    status, output = commands.getstatusoutput(cmd)
    print output.strip()
    # print cmd
