#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
from util import *
from const import ph_table, sh_table,eh_table
from stream import io
import os
class Elf_Shdr:
    def __init__(self,arch,raw,off=None,**kw):
        self.arch=arch
        if off:
            data=raw[off:]
            if arch=="amd64":
                self.sh_name=u32(data[0:4])
                self.sh_type=u32(data[4:8])
                self.sh_flags=u64(data[8:16])
                self.sh_addr=u64(data[16:24])
                self.sh_offset=u64(data[24:32])
                self.sh_size=u64(data[32:40])
                self.sh_link=u32(data[40:44])
                self.sh_info=u32(data[44:48])
                self.sh_addralign=u64(data[48:56])
                self.sh_entsize=u64(data[56:64])
            else:
                self.sh_name=u32(data[0:4])
                self.sh_type=u32(data[4:8])
                self.sh_flags=u32(data[8:12])
                self.sh_addr=u32(data[12:16])
                self.sh_offset=u32(data[16:20])
                self.sh_size=u32(data[20:24])
                self.sh_link=u32(data[24:28])
                self.sh_info=u32(data[28:32])
                self.sh_addralign=u32(data[32:36])
                self.sh_entsize=u32(data[36:40])
            self.raw=raw[self.sh_offset:self.sh_offset+self.sh_size]
        else:
            kw["sh_type"]=sh_table.inv[kw["sh_type"]]
            self.__dict__.update(kw)
            self.raw=raw

    def __len__(self):
        if self.arch=="amd64":
            return 64
        else:
            return 40

    @staticmethod
    def size(arch):
        if arch == "amd64":
            return 64
        else:
            return 40

    def __get_type(self):
        return sh_table[self.sh_type]

    def __set_type(self,t):
        self.sh_type=sh_table.inv[t]

    type=property(__get_type,__set_type)

    def __str__(self):
        if self.arch=="amd64":
            ret=p32(self.sh_name)+p32(self.sh_type)+p64(self.sh_flags)+p64(self.sh_addr)+\
                    p64(self.sh_offset)+p64(self.sh_size)+p32(self.sh_link)+p32(self.sh_info)+\
                    p64(self.sh_addralign)+p64(self.sh_entsize)
        else:
            ret=p32(self.sh_name)+p32(self.sh_type)+p32(self.sh_flags)+p32(self.sh_addr)+\
                    p32(self.sh_offset)+p32(self.sh_size)+p32(self.sh_link)+p32(self.sh_info)+\
                    p32(self.sh_addralign)+p32(self.sh_entsize)
        return ret
