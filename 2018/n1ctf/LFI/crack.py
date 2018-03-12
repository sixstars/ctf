import array
import phoenixAES

def ary(x):
    return array.array('B', x)

import sys

traces = open(sys.argv[1]).read()

def fmt(x):
    return b''.join(b'%02X'%a for a in x)

with open('tracefile', 'wb') as f:
    for line in traces.strip().splitlines():
        a, b = [[int(y) for y in x.split(',')] for x in line.split()]
        f.write(b'%s %s\n'%(fmt(a),fmt(b)))

phoenixAES.crack('tracefile')

