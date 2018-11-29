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

class Elf_Phdr:
    def __init__(self,arch,data=None,**kw):
        self.arch=arch
        if data!=None:
            if arch=="amd64":
                self.p_type=u32(data[0:4])
                self.p_flags=u32(data[4:8])
                self.p_offset=u64(data[8:16])
                self.p_vaddr=u64(data[16:24])
                self.p_paddr=u64(data[24:32])
                self.p_filesz=u64(data[32:40])
                self.p_memsz=u64(data[40:48])
                self.p_align=u64(data[48:56])
            else:
                self.p_type=u32(data[0:4])
                self.p_offset=u32(data[4:8])
                self.p_vaddr=u32(data[8:12])
                self.p_paddr=u32(data[12:16])
                self.p_filesz=u32(data[16:20])
                self.p_memsz=u32(data[20:24])
                self.p_flags=u32(data[24:28])
                self.p_align=u32(data[28:32])
        else:
            kw["p_type"]=ph_table.inv[kw["p_type"]]
            self.__dict__.update(kw)

    def __str__(self):
        if self.arch=="amd64":
            ret=p32(self.p_type)+p32(self.p_flags)+p64(self.p_offset)+\
                    p64(self.p_vaddr)+p64(self.p_paddr)+p64(self.p_filesz)+\
                    p64(self.p_memsz)+p64(self.p_align)
        else:
            ret=p32(self.p_type)+p32(self.p_offset)+p32(self.p_vaddr)+p32(self.p_paddr)+\
                    p32(self.p_filesz)+p32(self.p_memsz)+p32(self.p_flags)+p32(self.p_align)
        return ret


    def __len__(self):
        if self.arch=="amd64":
            return 56
        else:
            return 32
    @staticmethod
    def size(arch):
        if arch == "amd64":
            return 56
        else:
            return 32

    def __get_type(self):
        return ph_table[self.p_type]

    def __set_type(self,t):
        self.p_type=ph_table.inv[t]

    type=property(__get_type,__set_type)

