#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
from util import *
from . import *
from stream import io
import os
class Elf_Ehdr:
    def __init__(self,header=None,**kw):
        if header !=None:
            self.e_magic=header[0:16]
            self.e_type=u16(header[16:18])
            self.e_machine=u16(header[18:20])
            self.e_version=u32(header[20:24])
            if self.arch == "amd64":
                self.e_entry=u64(header[24:32])
                self.e_phoff=u64(header[32:40])
                self.e_shoff=u64(header[40:48])
                idx=48
            else:
                self.e_entry=u32(header[24:28])
                self.e_phoff=u32(header[28:32])
                self.e_shoff=u32(header[32:36])
                idx=36
            self.e_flags=u32(header[idx:idx+4])
            self.e_ehsize=u16(header[idx+4:idx+6])
            self.e_phentsize=u16(header[idx+6:idx+8])
            self.e_phnum=u16(header[idx+8:idx+10])
            self.e_shentsize=u16(header[idx+10:idx+12])
            self.e_shnum=u16(header[idx+12:idx+14])
            self.e_shstrndx=u16(header[idx+14:idx+16])
        else:
            self.__dict__.update(kw)

    def __str__(self):
        if self.arch=="amd64":
            ret=self.e_magic+p16(self.e_type)+p16(self.e_machine)+p32(self.e_version)+p64(self.e_entry)+\
                    p64(self.e_phoff)+p64(self.e_shoff)+p32(self.e_flags)+p16(self.e_ehsize)+p16(self.e_phentsize)+\
                    p16(self.e_phnum)+p16(self.e_shentsize)+p16(self.e_shnum)+p16(self.e_shstrndx)
        else:
            ret=self.e_magic+p16(self.e_type)+p16(self.e_machine)+p32(self.e_version)+p32(self.e_entry)+\
                    p32(self.e_phoff)+p32(self.e_shoff)+p32(self.e_flags)+p16(self.e_ehsize)+p16(self.e_phentsize)+\
                    p16(self.e_phnum)+p16(self.e_shentsize)+p16(self.e_shnum)+p16(self.e_shstrndx)
        return ret

    def __len__(self):
        if self.arch=="amd64":
            return 0x40
        else:
            return 0x34

    @staticmethod
    def size(arch):
        if arch=="amd64":
            return 0x40
        else:
            return 0x34

    def __get_type(self):
        return eh_table[self.e_type]

    def __set_type(self,t):
        self.e_type=eh_table.inv[t]
    type = property(__get_type,__set_type)

    @property
    def arch(self):# TODO only support i386 and amd64
        return "i386" if self.e_magic[4] == '\x01' else "amd64"

class Elf_Phdr:
    def __init__(self,arch,data=None,**kw):
        self.arch=arch
        if data:
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

class Elf_Shdr:
    def __init__(self,arch,data=None,**kw):
        self.arch=arch
        if data:
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
        else:
            kw["sh_type"]=sh_table.inv[kw["sh_type"]]
            self.__dict__.update(kw)

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

class Elf:
    def __init__(self,file_name=None,**kw):
        if file_name!= None:
            self.load_file(file_name)
        else:
            self.header=Elf_Ehdr(kw)
    
    def load_file(self,path):
        with open(file_name,"r") as f:
            self.raw=f.read()
        self.io=io(self.raw)
        self.header=Elf_Ehdr(self.raw)
        self.phdrs=[]
        self.address=None
        for i in range(self.header.e_phnum):
            tmp = Elf_Phdr(self.arch,self.raw[self.header.e_phoff+i*Elf_Phdr.size(self.arch):])
            self.phdrs.append(tmp)
            if tmp.type == "PT_LOAD"  \
                    and tmp.p_vaddr&0xfff==0 \
                    and self.address == None:
                self.address=tmp.p_vaddr
        self.shdrs = []
        for i in range(self.header.e_shnum):
            tmp=Elf_Shdr(self.arch,self.raw[self.header.e_shoff+i*Elf_Shdr.size(self.arch):])
            self.shdrs.append(tmp)
    @property
    def arch(self):
        return self.header.arch
    
    def add_phdr(self,phdr):
        self.phdrs.append(phdr)
        self.header.e_phnum+=1
        self.phdrs[0].p_memsz = self.header.e_phnum * Elf_Phdr.size(self.arch)
        self.phdrs[0].p_filesz = self.header.e_phnum * Elf_Phdr.size(self.arch)

    def add_shdr(self,shdr):
        self.shdrs.append(shdr)
        self.header.e_shnum+=1
        

    def locate_phoff(self,off):
        self.header.e_phoff = off
        self.phdrs[0].p_paddr = off + self.address
        self.phdrs[0].p_vaddr = off + self.address
        self.phdrs[0].p_offset = off

    def locate_shoff(self,off):
        self.header.e_shoff = off
    
    def locate_shstrtab(self,t):
        return self.raw[self.shdrs[self.header.e_shstrndx].sh_offset:].find(t)

    def save(self,path):
        self.write(0,str(self.header))
        off = self.header.e_phoff
        step = Elf_Phdr.size(self.arch)
        for i in range(self.header.e_phnum):
            self.write(off + i*step, str(self.phdrs[i]))

        off = self.header.e_shoff
        step = Elf_Shdr.size(self.arch)
        for i in range(self.header.e_shnum):
            self.write(off + i*step, str(self.shdrs[i]))
        self.io.save(path)
        os.chmod(path,0o755)

    def write(self,off,data):
        self.io[off]=data
