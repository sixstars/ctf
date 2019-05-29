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
    p = subprocess.Popen(name, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    sys.stdout.write(read_until(p.stdout, 0x100))
    sys.stdout.flush()


import os,sys,signal,logging
class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

import string
def checkInput(data):
    pattern = string.digits + string.ascii_letters
    for ch in data:
        if ch not in pattern:
            return False

    return True

if __name__ == '__main__':

    sys.stdout = Unbuffered(sys.stdout)
    interact_timeout = 120
    #set alarm 60s and change workdir
    signal.alarm(interact_timeout)

    # proof_of_work()
    input_data = read_until(sys.stdin, 0x100, '\n')
    if checkInput(input_data) == True:
        exec_serv('./xx_warm_up ' + input_data)
    else:
        print "bad input"
