#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

data = open("./log","r").read().split("\n")[:-1]
array = map(int,data)

with open("./loc_417000","r") as f:
	loc = f.read()


for i in range(len(array)):
	print ord(loc[array[i]])