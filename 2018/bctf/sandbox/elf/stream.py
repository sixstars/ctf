#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
import os
from tempfile import TemporaryFile

class io:
    def __init__(self,data=""):
        self.stream = TemporaryFile(mode="w+b")
        self.stream.write(data)

    def __getitem__(self,key):
        self.stream.seek(key)
        return self.stream.read(1)

    def __setitem__(self,key,item):
        self.stream.seek(key)
        self.stream.write(item)
    
    def __str__(self):
        self.stream.seek(0)
        return self.stream.read()

    def __len__(self):
        return len(self)

    def save(self,path):
        with open(path,"w+",) as f:
            f.write(str(self))

