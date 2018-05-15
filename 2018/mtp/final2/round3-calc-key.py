#!/usr/bin/env python
# coding:utf-8

import struct


def lcm(a, b):
    return a * b / egcd(a, b)[0]


def egcd(a, b):
    x, y, u, v = 0, 1, 1, 0
    while a != 0:
        q, r = b / a, b % a
        m, n = x - u * q, y - v * q
        b, a, x, y, u, v = a, r, u, v, m, n
    gcd = b
    return gcd, x, y


def chinese_reminder(mods, rems):
    n, m = mods
    a, b = rems
    _gcd, u, v = egcd(n, m)
    if abs(a - b) % _gcd:
        return None
    x1 = u * ((b - a) / _gcd)
    return n * x1 + a


def my_lcm(*arg):
    arg = list(arg)
    while len(arg) > 1:
        arg.append(lcm(arg.pop(), arg.pop()))
    return arg[0]


def my_chinese_remainder(pairs):
    while len(pairs) > 1:
        m1, r1 = pairs.pop()
        m2, r2 = pairs.pop()
        m0 = lcm(m1, m2)
        r0 = chinese_reminder((m1, m2), (r1, r2))
        pairs.append((m0, r0 % m0))
    return pairs[0][1]


def decomposition(x, n):
    res = []
    for _ in xrange(n):
        res.append(x % 64)
        x /= 64
    return res


def combine(x):
    tzb = 'VChf+BoN8qw43JzinLRQm95F/u7D6M0bYIeSTypAktsjOgWE2dUHrlGaPK1cZXvx'
    res = 0
    for i in x[::-1]:
        res = res * 64 + tzb.index(i)
    return res


def bf_x(k1):
    for x in xrange(0x7fff):
        if k1 == 8 * x**3 + 13 * x**2 + 26 * x + 87:
            return x
    raise Exception('x not found')


def calc_y(k2, k3, k4):
    assert k2 % 256 == 0
    m1 = 61454
    r1 = k2 / 256
    assert r1 < 61454

    m2 = 54732
    r2 = k3 % (256 * 256)

    m3 = 25548
    r3 = k4 / 256

    m4 = 5136
    r4 = k4 % 256 * 256 + k3 / (256 * 256)
    y = my_chinese_remainder([(m1, r1), (m2, r2), (m3, r3), (m4, r4)])
    return y


enc = 'ETKdgxteV6FHLzDCwmaVb9pYU5kSV6paNicOnO/wA0ZzM4CzVmALImn0CmxRhx0xSq/jV3Ad9i6s4+jQF0TUY3vCVm2obdcm8OozofmjlnCCVPBoT7qk+2n+bzN+jhz6VPJEw8OkfkuCoGRJRlftVYv+6uwKRYPza/RnlFVfVkgw+zofoVN8p1MPmI1WV6JUD2PnN3IBU4B3dEhCVPU0Z9f0oV7QFGpWJq0IVnzbhay2fkzLbrnQ4fCCV/J5GGpB4/RRNFpEEDhCV3yqFqXVoZX8brnQ4fCCVPiEP0fK8YN4F0K0k5CjV++eLc6BJ+oqhxo0pthCVkQG3D+8hYLRp96Kge8/VVsS2poXCnN9p1MPmI1WVkibZhh2+ne8oTsV82sgV+WTB1FIV+soomcyLBPWVmB7fWZ/N6goo5eD9MP0V88SnGo+qVMBoGRJRlftVYBL33+lBVWqFzIcSDYYV+o3M2F1++4iUOo3QIlbV6iyITQzRTRqoQE/POgBVO9jyGn0o+/iUj9rYop+VOyaiUU/NOimEjIz90M8VY0h7ZSVfk25Nga5DP8BVVubYGCgV29oEB/cQdhCV/0sv9STR/lfUaoit/N2V6f0dLQWnmK5aGLJ5CV0VVHgnkhch2RJFGVmkPyHVZep9hMvqmNfFveis+ypVrDrqVnUoTHop1o1HCJsVY9czBjc88+3bYfUGVUSVm9rQwUI+3IJEXcDKqnsV8o3m1V6hVZfUaoiEm4sV2k48R8YBnLCit16Z6WSVPT40lOgq/c3b2CfswUIVOdKMmRBiT+4bzntqb2SV6VAE2KmV6HQU4JOQ532VYc+WJsOz/j8brnQ4fCCVr48iac8J6jCoGRJRlftVOr3a9Gkf6jhiuDhZKifVrFVaeKjN6k3bpq/XxB/V8ymVYV94Y1hU4B3dEhCVT+cSfZNwOgiF5GfL1ILV+m4jUUD46aqo5OMT1shVkIlYEo2n2MBhxo0pthCV2QYkCN+L2OJF0K0k5CjVO0wL3FKB+eQFvi58sUEVZYVNhriQ38LFvi58sUEVkFCTg4WNY0oEXOskiCrVZN4XaL3B+89xlpIdJB2V2S/ocTJq/W8A8KTorrbVkNrn+Vu+neRhxo0pthCVZ+3bwr33Zahx8p2UkETVT0ruIFl4TLVFvi58sUEV8bRki8oo2hQbvo5FPJsVTmYHsddi6X4hxiXaAotVY+QZj+dJVg4U4tnHhooVVVVVVVVVVVV'

dec = ''
for i in xrange(0, len(enc), 20):
    cur = enc[i:i + 20]
    k1 = combine(cur[:8])
    k2 = combine(cur[8:][:4])
    k3 = combine(cur[12:][:4])
    k4 = combine(cur[16:][:4])
    x = bf_x(k1)
    y = calc_y(k2, k3, k4)
    dec += struct.pack('<Q', x)[:2]
    dec += struct.pack('<Q', y)[:6]

print dec
