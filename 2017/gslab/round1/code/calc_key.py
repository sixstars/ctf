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
    useless_func_addr = p.entry + 0x7F70
    p.hook(useless_func_addr, angr.Hook(simuvex.SimProcedures['stubs']['ReturnUnconstrained']), kwargs={'resolves': 'nothing'})
    useless_addr = p.entry + 0xA977
    redirect_addr = p.entry + 0xAA10
    # p.hook(useless_addr, angr.Hook(simuvex.SimProcedures['stubs']['Redirect'], redirect_to=redirect_addr), kwargs={'resolves': 'nothing'})
    # def go(state):
    #     state.regs.ip = redirect_addr
    #     print 'fuck', state.regs.ip
    # p.hook(useless_addr, angr.Hook(simuvex.SimProcedures['stubs']['UserHook'], user_func=go, length=2))

    start_addr = p.entry + 0xA41D
    aim_addr = p.entry + 0xAA50

    state = p.factory.blank_state(addr=start_addr)
    x = []
    for i in xrange(32):
        # x.append(state.se.BVS('x{}'.format(i), 8))
        x.append(state.se.BVV(key[i], 8))

    state.memory.store(state.regs.sp + 0x50, 0xAA000000, endness=state.arch.memory_endness)
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
    seed = s.se.any_int(s.regs.eax)
    return seed
