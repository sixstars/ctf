#!/usr/bin/env python
# coding:utf-8

from Crypto.Cipher import AES

from ctf import *


def purify(s):
    return ''.join(s.split())

def encrypt(key, msg):
    msg = unhex(msg)
    key = unhex(key)
    return enhex(AES.new(key, mode=AES.MODE_CBC, IV=key).encrypt(msg))

def decrypt(key, encrypted):
    encrypted = unhex(encrypted)
    key = unhex(key)
    return enhex(AES.new(key, mode=AES.MODE_CBC, IV=key).decrypt(encrypted))

def do_xor(msg, x):
    msg = unhex(msg)
    s = ''.join([chr(x + i) for i in xrange(len(msg))])
    return enhex(xor(msg, s))

def remove_padding(s):
    s = unhex(s)
    return enhex(s[:-ord(s[-1])])


aim = 'A04559D372B2917FCEA651A269E21EA5B7B6901059333F40CBF0EE0A785BD94BF6C028ADC9024D3A859FC3F8AB4E5FB1'
# aim = '74C3C238E74BE9B84F549259C187FBBDC88E1408316172B4C71665A9032BF873D7C8AEA5B54FD13E21C71D67A095CD24'
aim = do_xor(aim, ord('r'))
aim = do_xor(aim, ord('e'))
aim = do_xor(aim, ord('w'))
aim = do_xor(aim, ord('q'))
aim = do_xor(aim, ord('&'))
aim = do_xor(aim, ord('^'))

print aim
# exit()

# SM4 decrypt aim with key
key = '6B8C45BEE7CEA2EB05322199A0BB0BA2'
aim = '95078c6186c70d9b917f1d6d621830a9398788D488ED7433FDEDBB6C8538E13010101010101010101010101010101010'

aim = remove_padding(aim)
print aim
aim = do_xor(aim, ord(')'))
print aim

aim = do_xor(aim, ord('*'))
key = '6B8C45BEE7CEA2EB05322199A0BB0BA2'
aim = decrypt(key, aim)
print aim
aim = remove_padding(aim)

aim = do_xor(aim, 38)
aim = do_xor(aim, 36)
aim = do_xor(aim, 64)
aim = do_xor(aim, 33)
print aim
print unhex(aim)