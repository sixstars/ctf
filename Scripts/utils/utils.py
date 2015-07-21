#!/usr/bin/env python
#encoding:utf-8

import os
import signal

from pwn import *

__all__ = ['SET_PAD_CHAR', 'NOPS', 'LEFT_PAD', 'RIGHT_PAD', 'debug']

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

def debug(args, shell=False, executable=None, cwd=None, env=None, timeout=pwnlib.timeout.Timeout.default):
    if type(args) == str:
        args = [args]
    args = ['gdb'] + args
    io = process(args, shell, executable, cwd, env, timeout)
    io.sendline('set prompt {0} '.format(term.text.bold_red('gdb$')))
    return io

def ext_interactive(self, prompt = ''):
    """interactive(prompt = '')
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

pwnlib.tubes.tube.tube.ext_interactive = ext_interactive
