from pwn import *

val = {}
used = {}


def format_code(code_list, code):
    res = []
    for idx, opcode, operands in code_list:
        if len(operands) > 3:
            print code[int(idx) - 5:int(idx) + 5]
            raise Exception()
        if opcode == 'leal':
            src1, src2 = operands[0][1:-1].replace('r', 'e').split(',')
            operands = [src1, src2, operands[1]]
        res.append((idx, opcode, operands))
    return res


def remove_dup(code_list):
    val.clear()
    res = []
    for idx, opcode, operands in code_list:
        if opcode == 'movl':
            src, dst = operands
            if src not in val:
                val[src] = src
            if val[src] == val.get(dst):
                continue
            val[dst] = val[src]
        else:
            if len(operands) == 1:
                src = operands[0]
                dst = src
                src2 = src
            elif len(operands) == 2:
                src, dst = operands
                src2 = src
            elif len(operands) == 3:
                src, src2, dst = operands
            else:
                raise Exception('too many operands: %s %s' % (opcode, operands))
            if src not in val:
                val[src] = src
            if src2 not in val:
                val[src2] = src
            val[dst] = idx
        res.append([idx, opcode, operands])
    print 'remove dup from %d to %d' % (len(code_list), len(res))
    return res


def remove_dead(code_list):
    used.clear()
    used['%eax'] = True
    res = []
    for idx, opcode, operands in code_list[::-1]:
        if len(operands) == 1:
            src = operands[0]
            dst = src
            src2 = src
        elif len(operands) == 2:
            src, dst = operands
            src2 = src
        elif len(operands) == 3:
            src, src2, dst = operands
        else:
            raise Exception('too many operands: %s %s' % (opcode, operands))
        if not used.get(dst, False):
            continue
        if opcode == 'movl':
            used[dst] = False
        else:
            used[dst] = True
        used[src] = True
        used[src2] = True
        res.append([idx, opcode, operands])
    res = res[::-1]
    print 'remove dead from %d to %d' % (len(code_list), len(res))
    return res


def do_analysis(code, floor, upper, cu, r):
    c = code.split('\n')
    code = []
    for i in c:
        code.append(i.split('\t'))
    code = code[:-2]
    t_code = []
    d_l = []
    for c in code:
        t_code.append([c[0], c[1], c[-1].split(', ')])
        d_l.append(c[0])
    t_code = t_code[floor - 1:upper][::-1]

    m = []
    for i in t_code:
        if i[1] not in m:
            m.append(i[1])
    taint = ['%eax']
    c = 0
    dup_l = []
    rem_l = []
    for i in t_code:
        if len(i[2]) == 1:
            continue
        if i[2][1] in taint:
            if i[1] == 'movl':
                taint.remove(i[2][1])
            if i[1] == 'leal':
                taint.remove(i[2][1])
                taint += i[2][0][1:-1].replace('r', 'e').split(',')
            else:
                taint.append(i[2][0])
            rem_l.append(i[0])
            dup_l.append(i)

    dup_l = dup_l[::-1]
    dup_l = format_code(dup_l, code)
    # while True:
    #     old_dup_l = dup_l
    #     dup_l = remove_dup(dup_l)
    #     dup_l = remove_dead(dup_l)
    #     if len(dup_l) == len(old_dup_l):
    #         break
    dup_l = remove_dup(dup_l)
    dup_l = remove_dead(dup_l)

    id_list = [c[0] for c in dup_l]
    for i in t_code:
        if i[0] not in id_list:
            r.sendline(i[0])

    return m, len(dup_l)


def reg_s(dl):
    o = [dl[0]]
    tmp_n = int(dl[0])
    for i in dl[1:-1]:
        if int(i) - tmp_n != 1:
            if int(o[-1]) != tmp_n:
                o[-1] = o[-1] + '-' + str(tmp_n)
            o.append(i)
        tmp_n = int(i)
    if int(dl[-1]) - tmp_n != 1:
        if int(o[-1]) != tmp_n:
            o[-1] = o[-1] + '-' + str(tmp_n)
        o.append(dl[-1])
    else:
        o[-1] = o[-1] + '-' + dl[-1]
    return o


r = remote('coconut.chal.pwning.xxx', 6817)
cou = 0
while (True):
    r.recvuntil('threshold required <= ')
    threshold = int(r.recvline().replace('\n', ''))
    r.recvline()
    code = r.recvuntil('<<<EOF>>>\n')

    r.recvuntil('only be >=')
    floor = r.recvuntil('and <=')
    floor = int(floor.split(' ')[0])
    upper = int(r.recvline().replace(':\n', ''))
    m, c = do_analysis(code, floor, upper, cou, r)
    cou += 1
    r.sendline('#')
    if cou == 51:
        context.log_level = 'debug'
    print m
    print cou, threshold, floor, upper, len(code.split('\n')) - 2, c

#r.recv(1024)

print threshold, floor, upper
r.interactive()
