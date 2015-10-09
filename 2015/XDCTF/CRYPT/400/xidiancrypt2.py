import random,sys,struct
import SocketServer
import base64 as b64
import hmac
from time import time
import math
import array,binascii
import collections
from hashlib import sha512,sha1
import SocketServer,os
from subprocess import Popen, PIPE
import threading
from secret import FLAG

KEY = [263, 327]
ENC_FLAG = "85b3e32c9825ce21133ea8afc22f9eb575fbfe947900c89b682b28e68c73c9f0042b27766d5e2de33ea8a95037ae50048701ec5225a9360d9163ba61f4747d828a1c420b0692b426f"

M = 12 
N = M * 2
K = N
numrounds = 2 ** 24 

def genSbox(seed="today is a good day"):
  fSub = {}
  fInvSub = {}
  i = 0
  prng = sha512()
  prng.update(seed)
  seed = prng.digest()
  cSeed = ""
  for x in xrange(2048):
    cSeed+=prng.digest()
    prng.update(str(x)+prng.digest())
  unused = range(2**M)
  for x in xrange(0,2**(M+1),2):
    curInd = (ord(cSeed[x]) + (ord(cSeed[x + 1]) << 8)) % len(unused)
    toDo = unused[curInd]
    del unused[curInd]
    fSub[x / 2] = toDo
    fInvSub[toDo] = x / 2
  return fSub, fInvSub

f, fInv = genSbox()
f2, fInv2 = genSbox("today is not a good day")

def F(s, k):
  return f[s ^ k]

def F2(s, k):
  return f2[s^k]

def FInv(s, k):
  return fInv[s] ^ k

def F2Inv(s, k):
  return fInv2[s] ^k

def get_key(key, n):
  return key[n & 1]

def encrypt_single_block(plaintext, key):
  txt = plaintext
  l, r = (txt >> M) & ((1 << M) - 1), txt & ((1 << M) - 1)
  for x in xrange(numrounds):
    l1 = r
    r1 = l ^ F(r, key[0])
    r2 = r ^ F2(r1, key[1])
    l, r = l1, r2
  return l << M | r

def decrypt_single_block(ciphertext, key):
  txt = ciphertext
  l, r = (txt >> M) & ((1 << M) - 1), txt & ((1 << M) - 1)
  for x in xrange(numrounds):
    r0 = l
    r1 = F2Inv( l ^ r ,key[1]) 
    l0 = r1 ^ F(r0, key[0])
    l, r = l0, r0
  return l << M | r

def extract(s):
  c = 0
  for x in s:
    c = (c << 8) | ord(x)  
  return c

def intract(n):
  s = []
  while n > 0:
    s.append(chr(n & 0xff))
    n = n >> 8
  return ''.join(s[::-1])

def get_blocks(txt):
  n = N / 8
  if len(txt) % n != 0:
    txt += '\x00' * (n - len(txt) % n) 
  block_strs = [txt[i*n:i*n+n] for i in range(len(txt) / n)]
  return [extract(s) for s in block_strs]

def unblocks(l):
  z = [intract(x) for x in l]
  s = ''.join(z)
  s = s.strip('\x00')
  return s


def encrypt(plaintext):
  blocks = get_blocks(plaintext)
  ars = [str(len(blocks))] + [str(block) for block in blocks]
  enc_process = Popen(["./cVerCrypt", str(KEY[0]), str(KEY[1])], stdin=PIPE, stdout=PIPE)
  (output, _) = enc_process.communicate("\n".join(ars) + "\n")
  output = map(int, output.split('\n')[:-1])
  return unblocks(output)

def decrypt(ciphertext):
  blocks = get_blocks(ciphertext)
  out = [decrypt_single_block(block, KEY) for block in blocks]
  return unblocks(out)

class XidianCryptoService(SocketServer.BaseRequestHandler):
  def handle(self):
    req = self.request
    req.sendall("Welcome to use XidianCryptoService!\n")
    req.sendall(ENC_FLAG + '\n')
    req.sendall("Send your encryption string: \n")
    data = req.recv(2049)[:-1].decode('hex')
    resp = encrypt(data)
    req.sendall(resp.encode('hex') + '\n')
    req.close()

class ThreadedServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
  pass

def checkKey():
  global ENC_FLAG
  print "checking key..."
  valid = True
  process = Popen(["./check", str(KEY[0]), str(KEY[1])], stdin=PIPE, stdout=PIPE)
  blocks = get_blocks(FLAG)
  try:
    (output, _) = process.communicate("\n".join([str(len(blocks))] + [str(x) for x in blocks]))
  except:
    valid = False
  if valid:
    ENC_FLAG = output.strip('\n')
  return valid

def updateKey():
  global KEY
  print "Changing key..."
  print "Old key:", KEY
  KEY = [random.randint(0, (1 << (K >> 1)) - 1), random.randint(0, (1 << (K >> 1)) -1)]
  while not checkKey():
    KEY = [random.randint(0, (1 << (K >> 1)) - 1), random.randint(0, (1 << (K >> 1)) -1)]
  print "New key:", KEY
  print "New ENC_FLAG:", ENC_FLAG
  threading.Timer(10* 60, updateKey, []).start()

if __name__ == "__main__":
  HOST, PORT = "0.0.0.0", 5678
  threading.Timer(1, updateKey, []).start()
  ThreadedServer.allow_reuse_address = True
  server = ThreadedServer((HOST, PORT), XidianCryptoService)
  server.allow_reuse_address = True
  server.serve_forever()

