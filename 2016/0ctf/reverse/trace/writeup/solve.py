#!/usr/bin/env python
# coding:utf-8

from ctf import *

data = list(string.lowercase + string.uppercase + string.digits + '{}')
data += map(lambda x: 'x' + str(x), xrange(26))
fp = open('trace_8339a701aae26588966ad9efa0815a0a.log')

less = {}
for i in data:
    less[i] = set()

def exchange(i, j):
    t = data[i]
    data[i] = data[j]
    data[j] = t

def simulate(base):
    i = base + 1
    j = base + 1
    while True:
        line = fp.readline()
        if line.startswith('[INFO]00400924'):
            i += 1
        elif line.startswith('[INFO]00400918'):
            less[data[i]].add(data[base])
            exchange(i, j)
            j += 1
        elif line.startswith('[INFO]00400940'):
            exchange(base, j - 1)
        elif line.startswith('[INFO]00400990'):
            simulate(base)
        elif line.startswith('[INFO]004009b4'):
            simulate(j)
        elif line.startswith('[INFO]004009cc'):
            return

simulate(0)

for i in data:
    print i, '->', less[i]

print data
