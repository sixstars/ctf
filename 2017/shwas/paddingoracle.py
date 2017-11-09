#! /usr/bin/python
#python exploit.py -c 4141414141414141414141414141414173f880342a533d069b3d2c33ea2c452aaac1cdf6ccb81e51f081a90ea411fe9edbd6bf6de7bab502dabdb9c51b7fb490 -l 16 -v


'''
    Padding Oracle Attack implementation of this article https://not.burntout.org/blog/Padding_Oracle_Attack/
    Check the readme for a full cryptographic explanation
    Author: mpgn <martial.puygrenier@gmail.com>
    Date: 2016
    Modifyed by hdt@2017-11-05
'''

import argparse
import httplib, urllib
import re
import binascii
import sys
import time
from binascii import unhexlify, hexlify
from itertools import cycle, izip

####################################
# CUSTOM YOUR RESPONSE ORACLE HERE #
####################################
from pwn import *
#context.log_level = ''
def test_validity(response):
    # oracle repsonse with data in the DOM
    data = response
    if data.find("bad") == -1:
        return 1
    return 0

################################
# CUSTOM YOUR ORACLE HTTP HERE #
################################
import socket
HOST = '106.75.98.74'
PORT = 10010 
s = remote(HOST, PORT)
def call_oracle(up_cipher):
    cipher = up_cipher.decode('hex')
    iv = cipher[:16].encode('base64')
    cipher = cipher[16:].encode('base64')
    s.send('3\n' + iv + cipher)
    data = s.clean(0.1)
    return 1, data

# the exploit don't need to touch this part
# split the cipher in len of size_block
def split_len(seq, length):
    return [seq[i:i+length] for i in range(0, len(seq), length)]

''' create custom block for the byte we search'''
def block_search_byte(size_block, i, pos, l):
    hex_char = hex(pos).split('0x')[1]
    return "00"*(size_block-(i+1)) + ("0" if len(hex_char)%2 != 0 else '') + hex_char + ''.join(l)    

''' create custom block for the padding'''
def block_padding(size_block, i):
    l = []
    for t in range(0,i+1):
        l.append(("0" if len(hex(i+1).split('0x')[1])%2 != 0 else '') + (hex(i+1).split('0x')[1]))
    return "00"*(size_block-(i+1)) + ''.join(l)

def hex_xor(s1,s2):
    return hexlify(''.join(chr(ord(c1) ^ ord(c2)) for c1, c2 in zip(unhexlify(s1), cycle(unhexlify(s2)))))

def run(cipher,size_block,host,url,cookie,method,post,error):
    cipher       = cipher.upper()
    found        = False
    result       = ['636c655f6d616b655f4145535f756e73','6563757265217d0a0808080808080808']
    valide_value = []
    len_block    = size_block*2
    cipher_block = split_len(cipher, len_block)

    if len(cipher_block) == 1:
        print "[-] Abort there is only one block"
        sys.exit()  
    #for each cipher_block
    for block in reversed(range(1,len(cipher_block)-2)):
        if len(cipher_block[block]) != len_block:
            print "[-] Abort length block doesn't match the size_block"
            break
        print "[+] Search value block : ", block, "\n"
        #for each byte of the block
        for i in range(0,size_block):
            # test each byte max 255
            for ct_pos in range(0,256):
                # 1 xor 1 = 0 or valide padding need to be checked
                if ct_pos != i+1 or (len(valide_value) > 0  and int(valide_value[-1],16) == ct_pos):

                    bk = block_search_byte(size_block, i, ct_pos, valide_value) 
                    bp = cipher_block[block-1]
                    bc = block_padding(size_block, i) 

                    tmp = hex_xor(bk,bp)
                    cb  = hex_xor(tmp,bc).upper()

                    up_cipher  = cb + cipher_block[block]
                    #time.sleep(0.5)

                    # we call the oracle, our god
                    connection, response = call_oracle(up_cipher)

                    if args.verbose == True:
                        exe = re.findall('..',cb)
                        discover = ('').join(exe[size_block-i:size_block])
                        current =  ('').join(exe[size_block-i-1:size_block-i])
                        find_me =  ('').join(exe[:-i-1])

                        sys.stdout.write("\r[+] Test [Byte %03i/256 - Block %d ]: \033[31m%s\033[33m%s\033[36m%s\033[0m" % (ct_pos, block, find_me, current, discover))
                        sys.stdout.flush()

                    if test_validity(response):

                        found = True
                        
                        # data analyse and insert in rigth order
                        value = re.findall('..',bk)
                        valide_value.insert(0,value[size_block-(i+1)])

                        if args.verbose == True:
                            print ''
                            #print "[+] HTTP ", response.status, response.reason
                            print "[+] Block M_Byte : %s"% bk
                            print "[+] Block C_{i-1}: %s"% bp
                            print "[+] Block Padding: %s"% bc
                            print ''

                        bytes_found = ''.join(valide_value)
                        if i == 0 and bytes_found.decode("hex") > hex(size_block) and block == len(cipher_block)-1:
                            print "[-] Error decryption failed the padding is > "+str(size_block)
                            sys.exit()

                        print '\033[36m' + '\033[1m' + "[+]" + '\033[0m' + " Found", i+1,  "bytes :", bytes_found
                        print ''

                        break 
            if found == False:
                # lets say padding is 01 for the last byte of the last block (the padding block)
                if len(cipher_block)-1 == block and i == 0:
                    value = re.findall('..',bk)
                    valide_value.insert(0,"01")
                    if args.verbose == True:
                        print ''
                        print '[-] No padding found, but maybe the padding is length 01 :)'
                        print "[+] Block M_Byte : %s"% bk
                        print "[+] Block C_{i-1}: %s"% bp
                        print "[+] Block Padding: %s"% bc
                        print ''
                        bytes_found = ''.join(valide_value)
                else:
                    print "\n[-] Error decryption failed"
                    result.insert(0, ''.join(valide_value))
                    hex_r = ''.join(result)
                    print "[+] Partial Decrypted value (HEX):", hex_r.upper()
                    padding = int(hex_r[len(hex_r)-2:len(hex_r)],16)
                    print "[+] Partial Decrypted value (ASCII):", hex_r[0:-(padding*2)].decode("hex")
                    sys.exit()
            found = False

        result.insert(0, ''.join(valide_value))
        valide_value = []

    print ''
    hex_r = ''.join(result)
    print "[+] Decrypted value (HEX):", hex_r.upper()
    padding = int(hex_r[len(hex_r)-2:len(hex_r)],16)
    print "[+] Decrypted value (ASCII):", hex_r[0:-(padding*2)].decode("hex")

if __name__ == '__main__':                           

    parser = argparse.ArgumentParser(description='Exploit of Padding Oracle Attack')
    parser.add_argument('-c', "--cipher",               required=True,              help='cipher you want to decrypt')
    parser.add_argument('-l', '--length_block_cipher',  required=True, type=int,    help='lenght of a block cipher: 8,16')
    parser.add_argument('--cookie',         help='Cookie example: PHPSESSID=9nnvje7p90b507shfmb94d7',   default="")
    parser.add_argument('--method',         help='Type methode like POST GET default GET',              default="GET")
    parser.add_argument('--post',           help="POST data example: 'user':'value', 'pass':'value'",    default="")
    parser.add_argument('-v', "--verbose",  help='debug mode, you need a large screen', action="store_true")
    args = parser.parse_args()

    run(args.cipher, args.length_block_cipher, HOST, None, args.cookie, args.method, args.post, None)
