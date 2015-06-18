#!/usr/bin/env python
#encoding:utf-8

import os
from collections import OrderedDict
from argparse import ArgumentParser
from tempfile import mktemp

def NOPS(n):
    return '\x90' * n

p = ArgumentParser()
p.add_argument('binary')
p.add_argument('hex_str')
args = p.parse_args()

# Normalize the length of the program name by making a symlink.
tmp_bin = './tmp.bin'
if os.path.exists(tmp_bin):
    os.remove(tmp_bin)
os.symlink(os.path.abspath(args.binary), tmp_bin)
os.execve(tmp_bin, [tmp_bin, args.hex_str.decode('hex')], {})
