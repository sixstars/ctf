#!/usr/bin/python
import random
import string
from hashlib import sha512
from Crypto.Util.number import *
from Crypto.Cipher import AES
import flag


def proof_of_work():
    proof = ''.join([random.choice(string.ascii_letters+string.digits)
                     for _ in xrange(20)])
    digest = sha512(proof).hexdigest()
    print_output("Proof of your work.\nsha512(%s+XXXX) == %s\n" %
                 (proof[:-4], digest))
    print_output('Tell me XXXX:')
    x = raw_input().strip()
    if len(x) != 4 or sha512(proof[:-4]+x).hexdigest() != digest:
        exit(1)
    print_output("OK, you proof.")
    return


def egcd(a, b):
    if (b == 0):
        return 1, 0, a
    else:
        x, y, q = egcd(b, a % b)
        x, y = y, (x - (a // b) * y)
        return x, y, q


def mod_inv(a, b):
    return egcd(a, b)[0] % b


def print_output(message):
    print(message)
    sys.stdout.flush()

def rsa_gen(bit_n=2048, bit_e=64):
    p = getPrime(bit_n/2)
    q = getPrime(bit_n/2)
    n = p*q
    e = getPrime(bit_e)
    d = mod_inv(e, (p-1)*(q-1))
    msg = int(''.join([random.choice(string.ascii_letters+string.digits)
                   for _ in xrange(16)]).encode('hex'), 16)
    cipher = pow(msg, e, n)
    return e, d, n, msg, cipher


def tell_n_d():
    e, d, n, m, c = rsa_gen()
    print_output("Give you a message:0x%x\nand its ciphertext:0x%x" % (m, c))
    print_output("Please give me the private key to decrypt cipher")
    print_output("n:")
    N = int(raw_input().strip())
    print_output("d:")
    D = int(raw_input().strip())
    if not pow(c, D, N) == m:
        exit(1)
    print_output("Oh, how you know the private key!")
    return m
    

def number_theory():
    while True:
        e, d, n, m, c = rsa_gen()
        print_output("n=0x%x\ne=0x%x\nc=0x%x\n" % (n, e, c))
        print_output("Now, you have a chance to decrypt something(but no c):")
        C = int(raw_input().strip())
        if C == c:
            print_output("Nonono~")
            continue
        M = pow(C, d, n)
        print_output("message:0x%x" % M)
        print_output("Give me right message:")
        MM = int(raw_input().strip())
        if not MM == m:
            exit(1)
        print_output("Master in math!")
        return m
        
def pad(s):
    return s + ((16-len(s)%16)*chr(16-len(s)%16))

def handle():
    #proof_of_work()
    msg1 = hex(tell_n_d())[2:-1].decode('hex')
    msg2 = hex(number_theory())[2:-1].decode('hex')
    cipher = AES.new(msg2, AES.MODE_CBC, msg1)
    enc = cipher.encrypt(pad(flag.flag))
    print_output("Here is your flag:0x%s" % enc.encode('hex'))


if __name__ == "__main__":
    handle()
