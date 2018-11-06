#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

s=['']*0x20
s[0] = 0x99
s[1] = 0xB0
s[2] = -121
s[3] = -98
s[4] = 112
s[5] = -24
s[6] = 65
s[7] = 68
s[8] = 5
s[9] = 4
s[10] = -117
s[11] = -102
s[12] = 116
s[13] = -68
s[14] = 85
s[15] = 88
s[16] = 0xB5
s[17] = 97
s[18] = -114
s[19] = 54
s[20] = -84
s[21] = 9
s[22] = 89
s[23] = -27
s[24] = 97
s[25] = -35
s[26] = 62
s[27] = 63
s[28] = -71
s[29] = 21
s[30] = -19
s[31] = -43

s=map(lambda x:x&0xff,s)
print "1"
print s
for _ in range(0x4):
    for i in range(0x20-1,0,-1):
        s[i]=s[i]^s[i-1]
print "2"
print s
for i in range(0x20):
    s[i]^=i
    s[i]=((s[i]>>2)&0xff)|((s[i]<<6)&0xff)

print "3"
print "".join(map(chr,s))






