#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.


with open("./traces","r") as f:
    data = f.read()
data = data.replace("\t"," ")
data = data.replace("\r","")
data = data.replace("\n\n","\n")

line_base = 10067
array = data.split("\n")[10067:14698+0x20]

pool = []
cnt=0


last = 0
delta = []
for i in range(len(array)):
    if "cyc" in array[i]:
        t = int(array[i].split(" ")[-1])
        if t > 100:
            print "cyc",i+line_base,t,i - last
            delta.append(i-last)
            last = i
            pool.append(i+line_base)

print delta
step = max(delta)*1.0/0x5e

print "".join(map(chr,[ int(i/step)+0x20  for i in delta]))

