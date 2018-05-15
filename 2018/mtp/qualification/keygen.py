#!/usr/bin/env python
# coding:utf-8

# from pwn import *
import random
import string
from lib import *


def transform_key(x):
    x = x.replace('#', '')
    x = x.upper()
    assert len(x) == 32
    x = ordlist(x)
    x = group(4, x)
    # printx
    # print hex( (x[0][0] * x[1][0] << 16) )
    # print hex( (x[0][0] * x[1][0] << 16) + (x[2][1] ^ x[0][1]) )
    # print hex( (x[0][0] * x[1][0] << 16) + (x[2][1] ^ x[0][1]) + (x[0][2] % (x[3][2] + 1) + 1) )
    # print hex( (x[0][0] * x[1][0] << 16) + (x[2][1] ^ x[0][1]) + (x[0][2] % (x[3][2] + 1) + 1) + x[0][3] / (x[4][3] + 1) )
    y0 = (x[0][0] * x[1][0] << 16) + (x[2][1] ^ x[0][1]) + (x[0][2] % (x[3][2] + 1) + 1) + x[0][3] / (x[4][3] + 1)

    # print hex( ((x[5][0] ^ x[1][0]) << 16) )
    # print hex( ((x[5][0] ^ x[1][0]) << 16) + x[1][1] % (x[6][1] + 3) )
    # print hex( ((x[5][0] ^ x[1][0]) << 16) + x[1][1] % (x[6][1] + 3) + (x[1][2] / (x[7][2] + 1) + 5) )
    # print hex( ((x[5][0] ^ x[1][0]) << 16) + x[1][1] % (x[6][1] + 3) + (x[1][2] / (x[7][2] + 1) + 5) + x[0][3] + x[1][3] )
    y1 = ((x[5][0] ^ x[1][0]) << 16) + x[1][1] % (x[6][1] + 3) + (x[1][2] / (x[7][2] + 1) + 5) + x[0][3] + x[1][3]

    # print x[2][0]
    # print x[1][3]
    # print hex( ((x[2][0] / x[1][3]) << 16) )
    # print hex( (((x[2][0] / x[1][3]) << 16) ^ (x[2][1] % x[3][1])) )
    # print hex( (((x[2][0] / x[1][3]) << 16) ^ (x[2][1] % x[3][1])) + x[5][2] + x[2][2] + 12 )
    # print hex( (((x[2][0] / x[1][3]) << 16) ^ (x[2][1] % x[3][1])) + x[5][2] + x[2][2] + 12 + x[7][3] + x[2][3] )
    # y2 = (((x[2][0] / x[1][3]) << 16) ^ (x[2][1] % x[3][1])) + x[5][2] + x[2][2] + 12 + x[7][3] + x[2][3]
    y2 = (((x[2][0] / (x[1][0] + 3)) << 16) ^ (x[2][1] % x[3][1])) + x[5][2] + x[2][2] + 12 + x[7][3] + x[2][3]

    y3 = a3 = x[2][3] ^ x[0][1]
    # print hex(y3)
    y3 *= x[3][1] + x[1][3]
    # print hex(y3)
    y3 &= x[5][2] & x[4][2]
    # print hex(y3)
    y3 = (y3 * x[7][3]) + y1
    y3 = y0 * x[6][0] * y3
    # print hex(y3)

    # print hex(y3 - y1)
    # print hex(y0 * 2)
    y3 = y3 - (y3 - y1) % (y0 * 2)
    # print hex(y3)

    y4 = (x[3][0] ^ x[4][0]) << 16
    y4 *= x[3][1] % (x[4][1] + 2)
    y4 += x[3][2] % (x[4][2] + 5) + 7
    y4 += x[3][3] * x[4][3]
    # print hex(y4)
    return y0, y1, y2, y3, y4


def calc_real_table():
    table = 'ZO6Kq79L&CPWvNopzQfghDRSG@di*kAB8rsFewxlm+/u5a^2YtTJUVEn0\x24HI34y#='
    change = [i ^ (i >> 3) for i in xrange(64)]
    pair = [(change[i], table[i]) for i in xrange(64)]
    pair = sorted(pair)
    return ''.join([x[1] for x in pair]) + '='


def calc_code(s):
# def calc_code(*args):
#     args = [x & ((1 << 64) - 1) for x in args]
#     s = flat(*args, word_size = 64)
    # print enhex(s)
    s = b64e(s)
    orig_tbl = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    new_tbl = calc_real_table()
    # print new_tbl
    s = ''.join([new_tbl[orig_tbl.index(c)] for c in s])
    return s


key = '0123#4567#8901#2345#6789#0123#4567#8901'
key = '#'.join(group(4, ''.join([random.choice(string.hexdigits) for i in xrange(32)])))
# key = '74af#32bF#8fcb#99A9#5CD8#aB78#a4Af#bDc0'.upper()

a1, a2, a3, a4, a5 = transform_key(key)

# a8 == a3 + (a5 * a1 + a2 - a4) * a5
a8 = a3 + (a5 * a1 + a2 - a4) * a5

# ((a6 * a1 + a2) * a6 + a3)  ==  a7
# (a2 - a4) * (a2 - a4) == 4 * a1 * (a6 * a4 + a3 - a7)

# (a2 - a4) * (a2 - a4) == 4 * a1 * x * a4 + 4 * a1 * a3 - 4 * a1 * x^2 * a1 - 4 * a1 * a2 * x - 4 * a1 * a3
# 4 * a1 * a1 *   x^2   +   (4 * a1 * a2 - 4 * a1 * a4)  *  x    =    - (a2 - a4) * (a2 - a4)
# (2 * a1 * x + a2 - a4) ^ 2 == 0
# 2 * a1 * x = a4 - a2
# print hex(a1)
# print hex(a4 - a2)
assert (a4 - a2) % a1 == 0
a6 = (a4 - a2) / (a1 * 2)
a7 = ((a6 * a1 + a2) * a6 + a3)
assert (a2 - a4) * (a2 - a4) == 4 * a1 * (a6 * a4 + a3 - a7)

# print hex(a1)
# print hex(a2)
# print hex(a3)
# print hex(a4)
# print hex(a5)
# print hex(((a6 * a1 + a2) * a6 + a3))
# print hex(a7)

# code = calc_code(a6, a7, a8, 0x32303138)
# print key
# print code

# print calc_code(0x3132333435363738, 0x3132333435363738, 0x3132333435363738, 0x3132333435363738)

# print 'key:', key
# print 'code:', code




SBOX = [156, 108, 244, 50, 174, 117, 159, 58, 79, 15, 217, 9, 90, 194, 203, 97, 123, 4, 226, 37, 157, 46, 35, 30, 219, 131, 92, 106, 183, 94, 196, 38, 190, 227, 21, 111, 86, 49, 254, 14, 186, 0, 109, 224, 158, 175, 208, 10, 115, 122, 120, 142, 153, 113, 232, 166, 99, 110, 134, 20, 13, 151, 150, 128, 173, 189, 72, 18, 176, 235, 202, 107, 82, 180, 53, 179, 93, 44, 42, 246, 155, 230, 162, 216, 137, 206, 221, 43, 68, 89, 240, 242, 169, 34, 127, 236, 64, 141, 164, 91, 143, 12, 177, 172, 70, 63, 163, 1, 170, 87, 28, 248, 241, 255, 129, 16, 187, 223, 96, 65, 195, 245, 209, 56, 215, 71, 31, 204, 193, 39, 130, 205, 238, 144, 77, 152, 211, 191, 229, 25, 112, 73, 182, 228, 185, 147, 29, 36, 138, 136, 145, 210, 118, 23, 105, 88, 104, 102, 22, 184, 126, 41, 5, 201, 60, 33, 146, 27, 161, 167, 253, 26, 231, 48, 51, 154, 84, 251, 8, 171, 135, 207, 165, 76, 95, 243, 249, 47, 3, 57, 252, 40, 139, 197, 66, 74, 55, 78, 148, 149, 212, 188, 62, 114, 237, 234, 116, 119, 59, 69, 52, 32, 192, 199, 140, 11, 103, 220, 98, 239, 45, 80, 19, 132, 225, 7, 75, 61, 6, 125, 214, 17, 100, 213, 160, 67, 178, 233, 2, 101, 181, 54, 24, 168, 222, 124, 250, 218, 81, 198, 133, 247, 83, 121, 200, 85]
INV_SBOX = [SBOX.index(i) for i in xrange(256)]
EXPAND_KEY = [99, 108, 101, 119, 103, 101, 109, 111, 98, 97, 108, 115, 56, 49, 48, 50, 227, 91, 114, 52, 132, 62, 31, 91, 230, 95, 115, 40, 222, 110, 67, 26, 78, 236, 38, 30, 202, 210, 57, 69, 44, 141, 74, 109, 242, 227, 9, 119, 73, 74, 231, 183, 131, 152, 222, 242, 175, 21, 148, 159, 93, 246, 157, 232, 195, 154, 65, 166, 64, 2, 159, 84, 239, 23, 11, 203, 178, 225, 150, 35, 20, 161, 65, 248, 84, 163, 222, 172, 187, 180, 213, 103, 9, 85, 67, 68, 185, 191, 20, 251, 237, 28, 202, 87, 86, 168, 31, 48, 95, 253, 92, 116, 248, 27, 66, 28, 21, 7, 136, 75, 67, 175, 151, 123, 28, 82, 203, 15, 34, 31, 89, 110, 55, 24, 209, 37, 116, 183, 70, 94, 104, 229, 141, 81, 203, 180, 55, 154, 252, 172, 230, 191, 136, 27, 160, 225, 224, 254, 45, 176, 57, 66, 238, 81, 197, 238, 8, 238, 77, 245, 168, 15, 173, 11, 133, 191]
MIX_TABLE = [14, 11, 13, 9, 9, 14, 11, 13, 13, 9, 14, 11, 11, 13, 9, 14]
INV_MIX_TABLE = []
for i in xrange(4):
    INV_MIX_TABLE += [3, 1, 1, 2][3 - i:]
    INV_MIX_TABLE += [3, 1, 1, 2][:3 - i]


def xor_list(a, b):
    return [a[i] ^ b[i] for i in xrange(len(a))]

def sub_bytes(data):
    return [SBOX[i] for i in data]

def inv_sub_bytes(data):
    return [INV_SBOX[i] for i in data]

def shift_row(data):
    res = []
    for i in xrange(4):
        t = data[i * 4:][:4]
        res += t[4 - i:]
        res += t[:4 - i]
    return res

def inv_shift_row(data):
    res = []
    for i in xrange(4):
        t = data[i * 4:][:4]
        res += t[i:]
        res += t[:i]
    return res

def fix_round_key(key):
    real_key = []
    for i in xrange(0, len(key), 4):
        real_key += key[i:i + 2]
        real_key.append(key[i + 3])
        real_key.append(key[i + 2])
    return real_key

def mix_column(data, mix):

    def mix_pow(x, n):
        assert n >= 0
        if n == 0:
            return x
        x *= 2
        if x > 0xff:
            x &= 0xff
            x ^= 0x1b
        return mix_pow(x, n - 1)

    def mix_poly(x, n):
        res = 0
        for i in xrange(4):
            if n & (1 << i):
                res ^= mix_pow(x, i)
        return res

    res = []
    for i in xrange(4):
        # col = [data[i], data[i + 4], data[i + 8], data[i + 12]]
        col = data[i * 4:][:4]
        for j in xrange(4):
            x = 0
            for k in xrange(4):
                x ^= mix_poly(col[k], mix[j * 4 + k])
            res.append(x)
    return res

def encrypt_block(data):
    round_key = fix_round_key(EXPAND_KEY[-16:])
    data = xor_list(data, round_key)
    for i in xrange(9, 0, -1):
        data = sub_bytes(data)
        data = shift_row(data)
        print 'after shift:', data
        data = mix_column(data, MIX_TABLE)
        print 'after mix:', data

        round_key = fix_round_key(EXPAND_KEY[i * 16:][:16])
        data = xor_list(data, mix_column(round_key, MIX_TABLE))

    data = sub_bytes(data)
    data = shift_row(data)
    data = xor_list(data, fix_round_key(EXPAND_KEY[:16]))
    # print map(hex, data)
    return data

def decrypt_block(data):
    data = xor_list(data, fix_round_key(EXPAND_KEY[:16]))
    data = inv_shift_row(data)
    data = inv_sub_bytes(data)

    for i in xrange(1, 10):
        round_key = fix_round_key(EXPAND_KEY[i * 16:][:16])
        data = xor_list(data, mix_column(round_key, MIX_TABLE))
        data = mix_column(data, INV_MIX_TABLE)
        data = inv_shift_row(data)
        data = inv_sub_bytes(data)

    round_key = fix_round_key(EXPAND_KEY[-16:])
    data = xor_list(data, round_key)
    # print data
    return data

def decrypt(data):
    res = ''
    for x in group(16, data):
        res += unordlist(decrypt_block(ordlist(x)))
    return res


# encrypt_block(ordlist('8765432187654321'))
# decrypt_block([23, 71, 30, 122, 40, 181, 244, 0, 107, 81, 20, 240, 80, 236, 135, 118])




args = [a6, a7, a8, 0x32303138]
args = [x & ((1 << 64) - 1) for x in args]
s = flat(*args, word_size = 64)

print 'key:', key

code = calc_code(s)
print 'standard code:', code

# print calc_code(0x3132333435363738, 0x3132333435363738, 0x3132333435363738, 0x3132333435363738)
code = calc_code(decrypt(s))
print 'advance code:', code

