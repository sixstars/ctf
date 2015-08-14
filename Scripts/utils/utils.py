#!/usr/bin/env python
#encoding:utf-8

import os
import signal

from pwn import *

__all__ = [
'factor', 'gcd', 'ext_euclid',
'SET_PAD_CHAR', 'NOPS', 'LEFT_PAD', 'RIGHT_PAD',
'debug'
]


#############################
### utils for calculation ###
#############################

def factor(n):
    """分解质因数"""
    while (2 < n) and (n & 1 == 0):
        n >>= 1
        print '2 * ',
    i = 3
    while i < n:
        if n % i == 0:
            n /= i
            print '%d *' % i,
            continue
        i += 2
    print n

def gcd(a, b):
    """最大公约数，a > b"""
    if b == 1:
        return a
    return gcd(b, a % b)

def ext_euclid(a, b):
    """扩展的欧几里德，a > b，ax+by=GCD(a, b) => x,y"""
    if a % b == 0:
        return 0, 1
    x, y = ext_euclid(b, a % b)
    return y, x - a / b * y


#############################
### utils for EXP writing ###
#############################

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


#######################
### utils for debug ###
#######################

def debug(args, shell=False, executable=None, cwd=None, env=None, timeout=pwnlib.timeout.Timeout.default):
    if type(args) == str:
        args = [args]
    args = ['gdb'] + args
    io = process(args, shell, executable, cwd, env, timeout)
    io.debug_mode = True
    io.sendline('set prompt {0} '.format(term.text.bold_red('gdb$')))
    return io

def gdb_break(self, addr):
    if type(addr) == int or type(addr) == long:
        self.sendline('b *0x{0:x}'.format(addr))
    else:
        self.sendline('b {0}'.format(addr))

def gdb_run(self):
    self.sendline('r')

def gdb_continue(self):
    self.sendline('c')

def ext_interactive(self, prompt = term.text.bold_red('$') + ' '):
    """interactive(prompt = pwnlib.term.text.bold_red('$') + ' ')
    Does simultaneous reading and writing to the tube. In principle this just
    connects the tube to standard in and standard out, but in practice this
    is much more usable, since we are using :mod:`pwnlib.term` to print a
    floating prompt.
    Thus it only works in while in :data:`pwnlib.term.term_mode`.
    """

    def handler(signum, frame):
        os.kill(proc.children(proc.pidof(self)[0])[0], signal.SIGINT)

    old_handler = signal.signal(signal.SIGINT, handler)

    log.info('Switching to extensive interactive mode')

    go = threading.Event()
    def recv_thread():
        while not go.isSet():
            try:
                cur = self.recv(timeout = 0.05)
                if cur:
                    sys.stderr.write(cur)
                    sys.stderr.flush()
            except EOFError:
                log.info('Got EOF while reading in interactive')
                break

    t = context.Thread(target = recv_thread)
    t.daemon = True
    t.start()

    try:
        while not go.isSet():
            if term.term_mode:
                if self.debug_mode:
                    data = term.readline.readline(prompt = '', float = True)
                else:
                    data = term.readline.readline(prompt = prompt, float = True)
            else:
                data = sys.stdin.readline()

            if data:
                # continue and exit interactive mode
                try:
                    if data.strip() == 'c!':
                        data = 'c\n'
                        go.set()
                    data = safeeval.const('"""{0}"""'.format(data.replace('"', r'\"')))
                    self.send(data)
                except ValueError:
                    log.warning('Illegal input, ignored!')
                except EOFError:
                    go.set()
                    log.info('Got EOF while sending in interactive')
            else:
                go.set()
    except KeyboardInterrupt:
        log.info('Interrupted')
        go.set()

    while t.is_alive():
        t.join(timeout = 0.1)

    signal.signal(signal.SIGINT, old_handler)

pwnlib.tubes.tube.tube.debug_mode = False
pwnlib.tubes.tube.tube.b = gdb_break
pwnlib.tubes.tube.tube.r = gdb_run
pwnlib.tubes.tube.tube.c = gdb_continue
pwnlib.tubes.tube.tube.ext_interactive = ext_interactive
