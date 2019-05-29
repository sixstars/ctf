#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
import angr,claripy,sys
p = angr.Project("./1.elf")
def hex(s):
    return "".join(["%02x"%ord(i) for i in s])
def xor_data(bs):
    s = ""
    for i in range(len(bs)):
        s+=chr(bs[i] ^ (0xe if i&1 else 0x19))
    return s


key = claripy.BVS('k',8*59)
st = p.factory.blank_state(addr = 0x02991923)
simgr = p.factory.simulation_manager(st)
simgr.use_technique(angr.exploration_techniques.DFS())

st.memory.store(0x2B934A0,key) 
sim = p.factory.simgr(st)
find = [0x2990D03]
avoid = [0x299195B]
sim.explore(find = find,avoid = avoid)

if sim.found:
    state = sim.found[0]
    out = state.se.eval(key,cast_to = bytes)
    print(out)
    data = hex(xor_data(out))
    print(data)
    with open("./input","w+") as f:
        f.write(data)
else:
    print("not found")


