#!/usr/bin/env python
# encoding:utf-8

import os
import signal

import pwn
from pwn import *

__all__ = [
    'factor', 'gcd', 'ext_euclid', 'rsa_decrypt',
    'ljust', 'rjust',
    'debug',
]

# export all imported from pwn
__all__ += [i for i in dir(pwn) if not i.startswith('__')]


#############################
### utils for calculation ###
#############################

def unhex(s):
    """Hex decode strings.
    Override unhex in pwntools.
    Hex-strings with odd length are acceptable.
    """
    s = str(s).strip()
    return (len(s) % 2 and '0' + s or s).decode('hex')


def factor(n):
    """Integer factorization (Prime decomposition)."""
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
    """Calculate greatest common divisor."""
    if b == 0:
        return a
    return gcd(b, a % b)


def ext_euclid(a, b):
    """Extended Euclidean algorithm. a > b, ax+by=GCD(a, b) => x,y"""
    if a % b == 0:
        return 0, 1
    x, y = ext_euclid(b, a % b)
    return y, x - a / b * y


def rsa_decrypt(c, e, p, q):
    """Decrypt RSA encrypted message when p and q are known."""
    # First calculate d.
    phi_n = (p - 1) * (q - 1)
    d, _ = ext_euclid(e, phi_n)
    d %= phi_n

    # Decrypt message using e.
    c_value = int(enhex(c), 16)
    n = p * q
    m = pow(c_value, d, n)
    m_hex = '%x' % m
    return unhex(m_hex)


#############################
### utils for EXP writing ###
#############################

def ljust(s, n, c=None):
    assert len(s) <= n
    if c is None:
        return s + cyclic(n - len(s))
    else:
        return s.ljust(n, c)


def rjust(s, n, c=None):
    assert len(s) <= n
    if c is None:
        return cyclic(n - len(s)) + s
    else:
        return s.rjust(n, c)


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


def _gdb_break(self, addr):
    if type(addr) == int or type(addr) == long:
        self.sendline('b *0x{0:x}'.format(addr))
    else:
        self.sendline('b {0}'.format(addr))


def _gdb_run(self):
    self.sendline('r')


def _gdb_continue(self):
    self.sendline('c')


def _gdb_interrupt(self):
    for child in proc.children(proc.pidof(self)[0]):
        os.kill(child, signal.SIGINT)


def _ext_interactive(self, prompt=term.text.bold_red('$') + ' '):
    """interactive(prompt = pwnlib.term.text.bold_red('$') + ' ')
    Does simultaneous reading and writing to the tube. In principle this just
    connects the tube to standard in and standard out, but in practice this
    is much more usable, since we are using :mod:`pwnlib.term` to print a
    floating prompt.
    Thus it only works in while in :data:`pwnlib.term.term_mode`.
    """

    def handler(signum, frame):
        self.interrupt()

    old_handler = signal.signal(signal.SIGINT, handler)

    log.info('Switching to extensive interactive mode')

    go = threading.Event()

    def recv_thread():
        while not go.isSet():
            try:
                cur = self.recv(timeout=0.05)
                if cur:
                    sys.stderr.write(cur)
                    sys.stderr.flush()
            except EOFError:
                log.info('Got EOF while reading in interactive')
                break

    t = context.Thread(target=recv_thread)
    t.daemon = True
    t.start()

    try:
        while not go.isSet():
            if term.term_mode:
                if self.debug_mode:
                    data = term.readline.readline(prompt='', float=True)
                else:
                    data = term.readline.readline(prompt=prompt, float=True)
            else:
                data = sys.stdin.readline()

            if data:
                # continue and exit interactive mode
                try:
                    if data.strip() == 'c!':
                        data = 'c\n'
                        go.set()
                    data = safeeval.const(
                        '"""{0}"""'.format(data.replace('"', r'\"')))
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
        t.join(timeout=0.1)

    signal.signal(signal.SIGINT, old_handler)


def _send(self, data):
    self._send(str(data))


def _sendline(self, data):
    self._sendline(str(data))


def _sendlines(self, data):
    for row in data:
        self.sendline(row)


pwnlib.tubes.tube.tube.debug_mode = False
pwnlib.tubes.tube.tube.b = _gdb_break
pwnlib.tubes.tube.tube.r = _gdb_run
pwnlib.tubes.tube.tube.c = _gdb_continue
pwnlib.tubes.tube.tube.interrupt = _gdb_interrupt

pwnlib.tubes.tube.tube._send = pwnlib.tubes.tube.tube.send
pwnlib.tubes.tube.tube.send = _send
pwnlib.tubes.tube.tube._sendline = pwnlib.tubes.tube.tube.sendline
pwnlib.tubes.tube.tube.sendline = _sendline
pwnlib.tubes.tube.tube.sendlines = _sendlines
pwnlib.tubes.tube.tube.ext_interactive = _ext_interactive
