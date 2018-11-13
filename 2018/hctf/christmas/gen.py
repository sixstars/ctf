#!/usr/bin/env python
import os, random,string

def gen_rnd_s(leng):
    return ''.join(random.sample(string.ascii_letters + string.digits, leng))

def gen_binary():
    with open('flag', 'r') as f:
        FLAG = f.read().strip()
    rnd_len = len(FLAG)-len('HCTFxy')

    code = '''
    #define _GNU_SOURCE
    #include <stdio.h>
    '''

    for i in xrange(random.randrange(10000)):
        code += 'char *  flag_err_1_{0}(){{return "HCTF{{{1}}}";}}\n'.format(i,gen_rnd_s(rnd_len))

    code += 'char * flag_yes_1337(){{return "{0}";}}\n'.format(FLAG)

    for i in xrange(random.randrange(10000)):
        code += 'char *  flag_err_2_{0}(){{return "HCTF{{{1}}}";}}\n'.format(i,gen_rnd_s(rnd_len))

    with open('./libflag.c', 'w') as f:
        f.write(code)

    os.system('gcc -o ./libflag.so ./libflag.c -fPIC -shared -ldl 2> /dev/null')

if __name__ == "__main__":
	gen_binary()

