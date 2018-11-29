#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
from util import *
from . import *
import os
class Elf:
    def __init__(self,file_name):
        with open(file_name,"r") as f:
            raw=f.read()
        self.io=io("")
        self.header=Elf_Ehdr(raw)
        self.phdrs=[]
        self.next_off = len(raw)
        for i in range(self.header.e_phnum):
            tmp_off =self.header.e_phoff+i*Elf_Phdr.size(self.arch)
            tmp = Elf_Phdr(self.arch,data=raw[tmp_off:tmp_off + Elf_Phdr.size(self.arch)])
            self.phdrs.append(tmp)

        self.shdrs = []
        for i in range(self.header.e_shnum):
            tmp=Elf_Shdr(self.arch,raw,off=self.header.e_shoff+i*Elf_Shdr.size(self.arch))
            self.shdrs.append(tmp)
        

    @property
    def arch(self):
        return self.header.arch
    
    def add_phdr(self,phdr):
        self.phdrs.append(phdr)
        self.header.e_phnum+=1
        #self.phdr.p_memsz = self.header.e_phnum * Elf_Phdr.size(self.arch)
        #self.phdr.p_filesz = self.header.e_phnum * Elf_Phdr.size(self.arch)

    def add_shdr(self,shdr):
        self.shdrs.append(shdr)
        self.header.e_shnum+=1
        
    def locate_shstrtab(self,t):
        shdr = self.shdrs[self.header.e_shstrndx]
        return shdr.raw.find(t)

    def save(self,path):
        self.write(0,str(self.header))
        off = self.header.e_shoff
        step = Elf_Shdr.size(self.arch)
        for i in range(self.header.e_shnum):
            self.write(off + i*step, str(self.shdrs[i]))
            self.write(self.shdrs[i].sh_offset,self.shdrs[i].raw)
        off = self.header.e_phoff
        step = Elf_Phdr.size(self.arch)
        for i in range(self.header.e_phnum):
            self.write(off + i*step, str(self.phdrs[i]))

        self.io.save(path)
        os.chmod(path,0o755)
    def write_code(self,address,code,flags=0x5):
        # only consider new seg
        pd=self.find_seg_base(address)
        if pd == None:
            self.write_code_in_new_seg(address,code,flags)
        elif pd.p_vaddr + pd.p_memsz < address + len(code):
            # alloc new off
            tmp = self.find_sec(pd.p_vaddr,pd.p_memsz)
            tmp.sh_offset = self.next_off
            tmp.sh_size = (address+len(code)-pd.p_vaddr+0xfff)>>12<<12
            off = address - tmp.sh_addr
            tmp.raw = (tmp.raw[:off]+code+tmp.raw[off+len(code):]).ljust(tmp.sh_size,"\x00")
            pd.p_offset = tmp.sh_offset
            pd.p_filesz = pd.p_memsz = tmp.sh_size
        else:
            tmp=self.find_sec(address,len(code))
            if tmp == None:
                raise Exception("can't find section to write")
            off = address - tmp.sh_addr
            tmp.raw = tmp.raw[:off]+code+tmp.raw[off+len(code):]
            
    def find_sec(self,add,length):
        for i in range(self.header.e_shnum):
            tmp = self.shdrs[i]
            if tmp.sh_addr<= add and add < tmp.sh_addr + tmp.sh_size and length <= tmp.sh_size:
                return tmp
        return None

    def write_code_in_new_seg(self,address,code,flags=0x5):
        size = ((address&0xfff) + len(code) + 0xfff)>>12<<12
        code = ((address&0xfff)*"\x00"+code).ljust(size,"\x00")
        new_shdr=Elf_Shdr(self.arch,raw = code,
                sh_type = "SHT_PROGBITS",
                sh_flags = 0x6,
                sh_name = self.locate_shstrtab(".text"),
                sh_addr = address>>12<<12,
                sh_offset = self.next_off,
                sh_size = size,
                sh_link = 0,
                sh_info = 0,
                sh_addralign = 0x10,
                sh_entsize = 0
                )
        self.add_shdr(new_shdr)
        self.next_off = new_shdr.sh_offset + new_shdr.sh_size
        new_phdr=Elf_Phdr(self.arch,
                p_type = "PT_LOAD",
                p_flags = flags,
                p_offset = new_shdr.sh_offset,
                p_vaddr = new_shdr.sh_addr,
                p_paddr = new_shdr.sh_addr,
                p_filesz = new_shdr.sh_size,
                p_memsz = new_shdr.sh_size,
                p_align = 0x200000
                )
        self.add_phdr(new_phdr)
    

    def write(self,off,code):
        self.io[off]=code

    def find_seg_base(self,addr):
        for i in range(self.header.e_phnum):
            tmp=self.phdrs[i]
            if tmp.type == "PT_LOAD" and\
                    (tmp.p_vaddr>>12<<12) <= addr and\
                    ((tmp.p_vaddr+tmp.p_memsz+0xfff)>>12<<12) > addr:
                return tmp
        return None
