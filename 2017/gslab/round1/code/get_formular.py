#!/usr/bin/env python
# coding:utf-8

import angr
import simuvex

# key = '0123-4567-89ab-cdef-0123-4567-89ab-cdef'
def calc(key):
    key = key.replace('-', '')
    assert len(key) == 32

    p = angr.Project('./libnative-lib.so')
    useless_func_addr = p.entry + 0x00050F00
    p.hook(useless_func_addr, angr.Hook(simuvex.SimProcedures['stubs']['ReturnUnconstrained']), kwargs={'resolves': 'nothing'})

    start_addr = p.entry + 0x00009B93
    aim_addr = p.entry + 0x0000A1AA

    state = p.factory.blank_state(addr=start_addr)
    x = []
    for i in xrange(32):
        # x.append(state.se.BVS('x{}'.format(i), 8))
        x.append(state.se.BVV(key[i], 8))

    state.memory.store(state.regs.sp + 0x40, 0xAA000000, endness=state.arch.memory_endness)
    state.memory.store(state.regs.bp + 0x10, 0xCC000000, endness=state.arch.memory_endness)
    state.memory.store(state.regs.bp + 0x14, 0xDD000000, endness=state.arch.memory_endness)
    state.memory.store(state.regs.bp + 0x18, 0xEE000000, endness=state.arch.memory_endness)
    state.memory.store(state.regs.bp + 0x1c, 0xFF000000, endness=state.arch.memory_endness)
    for i in xrange(8):
        str_addr = 0xBB000000 + i * 0x100
        state.memory.store(0xAA000000 + i * 4, str_addr, endness=state.arch.memory_endness)
        state.memory.store(str_addr - 4, 4, endness=state.arch.memory_endness)
        for j in xrange(4):
            state.memory.store(str_addr + j, x[i * 4 + j], endness=state.arch.memory_endness)

    path = p.factory.path(state)
    pg = p.factory.path_group(path)
    ex = pg.explore(find=aim_addr)
    # pg.explore(find=p.entry + 0x00009BE0)

    s = ex.found[0].state
    a1 = s.se.any_int(s.memory.load(0xCC000000, endness=state.arch.memory_endness))
    a2 = s.se.any_int(s.memory.load(0xDD000000, endness=state.arch.memory_endness))
    a3 = s.se.any_int(s.memory.load(0xEE000000, endness=state.arch.memory_endness))
    a6 = s.se.any_int(s.memory.load(0xFF000000, endness=state.arch.memory_endness))
    return a1, a2, a3, a6
