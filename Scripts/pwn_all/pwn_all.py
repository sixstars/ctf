#!/usr/bin/env python
#encoding:utf-8

import requests
import commands
import json
import time
import os

# This function should be replaced.
def submit_flag(flag):
    """
    True => Success
    False => Duplicate
    others => error info
    """
    import random
    return random.choice([True, False, 'error info'])

def submit_with_retry(flag, max_retry = 3):
    retry = 0
    result = ''
    while retry < max_retry:
        try:
            result = submit_flag(flag)
            if type(result) is bool:
                break
        except Exception, e:
            raise e
        retry += 1
        time.sleep(1)
    return result

def log(filename, msg):
    fp = open(filename, 'a')
    fp.write('[%s] %s\n' % (time.asctime(), str(msg).replace('\n', '; ')))
    fp.close()

def run_with_retry(cmd, max_retry = 2):
    retry = 0
    while retry < max_retry:
        status, output = commands.getstatusoutput(cmd)
        if status == 0:
            break
        retry += 1
    return status, output

def pwn(config):
    os.chdir(config['name'])
    log('out.log', 'PWN start')
    for i in config['ids']:
        cmd = config['cmd'].format(id=i)
        # status, flag = run_with_retry('timeout %d %s' % (config['timeout'], cmd))
        status, flag = run_with_retry('gtimeout %d %s' % (config['timeout'], cmd))
        if status == 0:
            result = submit_with_retry(flag)
            if result is True:
                log('out.log', '(ID = %d) %s' % (i, flag))
            elif result is not False:
                log('error.log', '(ID = %d) %s => %s' % (i, flag, result))
    log('out.log', 'PWN stop')

if __name__ == '__main__':
    while True:
        print '====== %s ======' % time.asctime()
        problems = json.load(open('config.json'))
        for config in problems:
            if os.fork() == 0:
                print 'PWN %s start' % config['name']
                pwn(config)
                print 'PWN %s stop' % config['name']
                exit()
        time.sleep(60)
