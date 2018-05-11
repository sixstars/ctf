#!/usr/bin/env python
# coding:utf-8

from ctf import *


def fix_method(method):
    lines = method.split('\n')
    to_remove = []
    for idx, row in enumerate(lines):
        if row.strip().startswith('return') or row.strip().startswith('goto'):
            for next_row in lines[idx + 1:]:
                next_row = next_row.strip()
                if next_row.startswith('goto'):
                    to_remove.append(next_row)
                    to_remove.append(next_row.split(' ')[1])
                if next_row.startswith(':'):
                    break

    ans = []
    print to_remove
    for row in lines:
        if row.strip() not in to_remove:
            ans.append(row)

    if to_remove:
        return fix_method('\n'.join(ans))
    return '\n'.join(ans)


def fix(p):
    src = read(p)
    method_list = src.split('.method')
    method_list = [fix_method(method) for method in method_list]
    fixed = '.method'.join(method_list)
    write(p, fixed)


for p in sys.argv[1:]:
    print 'fix:', p
    fix(p)
