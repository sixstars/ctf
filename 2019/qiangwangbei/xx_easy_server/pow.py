#!/usr/bin/python -u
# encoding: utf-8

import random, string, subprocess, os, sys
from hashlib import sha256

os.chdir(os.path.dirname(os.path.realpath(__file__)))

def proof_of_work():
    chal = ''.join(random.choice(string.letters+string.digits) for _ in xrange(16))
    sys.stdout.write(chal + "\n")
    sys.stdout.flush()
    sol = sys.stdin.read(4)
    if len(sol) != 4 or not sha256(chal + sol).hexdigest().startswith('00000'):
        exit()

def read_until(fd, max_sz, end_ch = None):
    data = ''
    while len(data) < max_sz:
        try:
            tch = fd.read(1)
        except Exception, e:
            break  

        if end_ch != None and tch == end_ch:
            break

        if tch == '':
            break      
        data += tch
        #print data
    return data

def exec_serv(name):
    p = subprocess.Popen(name, shell=True, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    p.communicate()


import os,sys,signal,logging
class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

if __name__ == '__main__':

    sys.stdout = Unbuffered(sys.stdout)
    interact_timeout = 120
    #set alarm 60s and change workdir
    signal.alarm(interact_timeout)

    proof_of_work()
    exec_serv('./xx_easy_server')
