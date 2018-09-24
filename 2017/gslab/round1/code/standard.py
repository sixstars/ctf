#!/usr/bin/env python
# coding:utf-8

import get_formular
import calc_key
import b64

key = input()
# key = '0123-4567-89ab-cdef-0123-4567-89ab-cdef'
a1, a2, a3, a6 = get_formular.calc(key)

import z3
a1 = z3.BitVecVal(0x12900088, 64)
a2 = z3.BitVecVal(0x000c00d3, 64)
a3 = z3.BitVecVal(0x00010c8f, 64)
a6 = z3.BitVecVal(0x00931487, 64)
a4 = z3.BitVec('a4', 64)
a5 = z3.BitVec('a5', 64)
s = z3.Solver()
s.add((a2 - a4) * (a2 - a4) - 4 * a1 * (a3 - a5) == 0)
s.add(a5 == a3 + (a2 + a6 * a1) * a6 - a6 * a4)
s.check()
a4 = s.model()[a4]
a5 = s.model()[a5]
# a4 = 0x6156a90cb031d043
# a5 = 0x66c3927c05467a87

from pwn import *
code = b64.encodeBase64(p64(a4) + p64(a5))
print code
