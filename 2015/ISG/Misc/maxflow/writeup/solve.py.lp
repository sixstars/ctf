#!/usr/bin/env python
# encoding:utf-8

from pulp import *

from utils import *

# context.log_level = 'debug'

io = remote('202.120.7.131', 9999)



def find_all_path(u):
    global visited
    visited[u] = True
    if u == 'T':
        global path, problem
        problem += lpSum(map(lambda e: e[2] * e[3], path)) <= 100.0
        visited[u] = False
        return
    global adjs
    for edge in adjs[u]:
        if not visited[edge[1]]:
            path.append(edge)
            find_all_path(edge[1])
            path.pop()
    visited[u] = False

def calc(edges):
    global adjs
    edges = map(lambda e: (e[0], e[1], e[2]), edges)
    nodes = map(lambda e: e[0], edges) + map(lambda e: e[1], edges)
    adjs = {}.fromkeys(nodes)
    nodes = adjs.keys()
    print nodes
    for key in adjs:
        adjs[key] = []

    for u, v, w in edges:
        x = LpVariable(u + '->' + v)
        # x = LpVariable(u + '->' + v, -w, w)
        adjs[u].append((u, v, w, x))
        adjs[v].append((v, u, w, -x))

    global problem
    problem = LpProblem("ISG maxflow", LpMaximize)
    aim = lpSum(map(lambda e: e[3], adjs['S']))
    problem += aim

    middle_nodes = filter(lambda x: x != 'S' and x != 'T', nodes)
    for u in middle_nodes:
        problem += lpSum(map(lambda e: e[3], adjs[u])) == 0

    global path, visited
    path = []
    visited = {}.fromkeys(nodes, False)
    find_all_path('S')

    problem.solve()
    return value(aim)


while True:
    io.recvuntil('Problem')
    print 'Problem', io.recvline()

    edges = []
    while True:
        if io.recv(2) != 'w[':
            break
        u = io.recvuntil('][', True)
        v = io.recvuntil('] = ', True)
        w = float(io.recvline(False))
        edges.append((u, v, w))
    io.recvuntil(':')

    print edges
    io.sendline(str(calc(edges)))

io.ext_interactive()
