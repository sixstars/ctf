#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
import PIL.Image as Image


im = Image.open("./GreatWall.png")

x,y = im.size
data = im.load()
"""
for i in range(x):
    for j in range(y):
        print i,j,map(hex,data[i,j])
"""
im.save("./tmp.png")


