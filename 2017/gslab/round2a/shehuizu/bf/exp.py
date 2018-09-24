#!/usr/bin/env python
# coding:utf-8

import zlib
import sys
import os
import struct
# from pwn import *

from forcecrc32 import crack_crc32

checksum = 0x614C5347

with open('libZapus.so') as fp:
    raw = fp.read()

def calc(s, v=0x811C9DC5):
    for c in s:
        v = (0x1000193 * (v ^ ord(c))) & 0xffffffff
    return v

init_crc = zlib.crc32(raw)
init_v = calc(raw)
print hex(init_v)
begin = int(sys.argv[1])
end = int(sys.argv[2])
fork_cnt = os.sysconf("SC_NPROCESSORS_ONLN")
print 'calc between {} and {} with {} processes'.format(begin, end, fork_cnt)
# part = (end - begin) / fork_cnt
children = []
# fork_cnt = 1
for j in xrange(fork_cnt):
    pid = os.fork()
    if pid != 0:
        children.append(pid)
        continue
    # for i in xrange(begin + j * part, begin + j):
    for i in xrange(begin + j, end, fork_cnt):
        # append = p32(i)
        append = str(struct.pack("<I", i))
        append += str(crack_crc32(append, checksum, init_crc=init_crc))
        print repr(append)
        v = calc(append, init_v)
        print hex(v)
        if i % 300000 == 0:
            print 'calced', i
        if v == checksum:
            print i
            os.system('echo {} >> found'.format(i))
            break
    exit()

print 'children:', children
for j in xrange(fork_cnt):
    # print 'ended:', os.waitpid(children[j], 0)
    print 'ended:' + str(os.wait())
