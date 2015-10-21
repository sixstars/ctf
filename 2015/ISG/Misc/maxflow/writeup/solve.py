#!/usr/bin/env python
# encoding:utf-8

import numpy
import scipy.linalg
from pulp import *

from utils import *

context.log_level = 'debug'


def calc(edges):
    global adjs
    edges = map(lambda e: (e[0], e[1], e[2]), edges)
    nodes = map(lambda e: e[0], edges) + map(lambda e: e[1], edges)
    adjs = {}.fromkeys(nodes)
    nodes = adjs.keys()
    nodes_count = len(nodes)
    print nodes

    tzb = {}
    new_id = 0
    for node in nodes:
        tzb[node] = new_id
        new_id += 1

    for key in adjs:
        adjs[key] = []
    for u, v, w in edges:
        adjs[u].append((tzb[u], tzb[v], w))
        adjs[v].append((tzb[v], tzb[u], w))

    middle_nodes = filter(lambda x: x != 'S' and x != 'T', nodes)
    coefficients = []
    for node in middle_nodes:
        equation = [0] * nodes_count
        for u, v, w in adjs[node]:
            per = 1 / w
            equation[u] += per
            equation[v] -= per
        coefficients.append(equation)

    problem = LpProblem("ISG maxflow", LpMaximize)
    voltages = [LpVariable('voltage-' + str(i)) for i in xrange(nodes_count)]

    equation = [0] * nodes_count
    equation[tzb['S']] = 1
    coefficients.append(equation)
    equation = [0] * nodes_count
    equation[tzb['T']] = 1
    coefficients.append(equation)

    coefficients = numpy.mat(coefficients)
    voltages = scipy.linalg.pinv(coefficients.T * coefficients) * coefficients.T * numpy.mat([[0]] * (nodes_count - 1) + [[100.0]])

    flow = 0
    for u, v, w in adjs['S']:
        flow += voltages[v] / w
    return float(flow)


io = remote('202.120.7.131', 9999)

while True:
    io.recvuntil('Problem')
    print 'Problem', io.recvline()

    edges = []
    while True:
        if io.recvuntil('w').strip() != 'w':
            break
        io.recv(1)
        u = io.recvuntil('][', True)
        v = io.recvuntil('] = ', True)
        w = float(io.recvline(False))
        edges.append((u, v, w))
    io.recvuntil(':')

    print edges
    max_flow = calc(edges)
    print 'max flow is:', max_flow
    io.sendline(str(max_flow))

io.ext_interactive()
