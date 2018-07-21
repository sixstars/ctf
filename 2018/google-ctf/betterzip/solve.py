import os
import zipfile
import zlib
import hashlib
from struct import pack, unpack
import sys

POLY_SZ = 20

f=open('flag.zip','rb')
f.read(0x16)
sz = unpack('I',f.read(4))[0]
f.read(12)

key_iv=f.read(20)
cipher_iv=f.read(20)
#print key_iv.encode('hex')
encdata=f.read(sz)
f.read(32)

def doxor(a,b):
  return map(lambda (x,y):x^y,zip(a,b))




class BitStream:
  def __init__(self, data, sz=None):
    if sz is None:
      sz = len(data) * 8

    self.sz = sz
    self.data = bytearray(data)
    self.idx = 0

  def get_bit(self):
    if self.idx >= self.sz:
      raise Exception('All bits used. Go away.')

    i_byte = self.idx / 8
    i_bit = self.idx % 8

    bit = (self.data[i_byte] >> i_bit) & 1
    self.idx += 1

    return bit

  def get_bits(self, sz):
    v = 0
    for i in xrange(sz):
      v |= self.get_bit() << i

    return v


class LFSR:
  def __init__(self, poly, iv, sz):
    self.sz = sz
    self.poly = poly
    self.r = iv
    self.mask = (1 << sz) - 1

  def get_bit(self):
    bit = (self.r >> (self.sz - 1)) & 1

    new_bit = 1
    masked = self.r & self.poly
    for i in xrange(self.sz):
      new_bit ^= (masked >> i) & 1

    self.r = ((self.r << 1) | new_bit) & self.mask
    return bit


class LFSRCipher:
  def __init__(self, key, poly_sz=8, key_iv=None, cipher_iv=None):
    if len(key) < poly_sz:
      raise Exception('LFSRCipher key length must be at least %i' % poly_sz)
    key = BitStream(key)

    if key_iv is None:
      key_iv = os.urandom(poly_sz)
    self.key_iv = key_iv
    key_iv_stream = BitStream(key_iv)

    if cipher_iv is None:
      cipher_iv = os.urandom(poly_sz)
    self.cipher_iv = cipher_iv
    cipher_iv_stream = BitStream(cipher_iv)

    self.lfsr = []
    for i in xrange(8):
      l = LFSR(key.get_bits(poly_sz) ^ key_iv_stream.get_bits(poly_sz),
               cipher_iv_stream.get_bits(poly_sz), poly_sz)
      self.lfsr.append(l)

  def get_keystream_byte(self):
    b = 0
    for i, l in enumerate(self.lfsr):
      b |= l.get_bit() << i
    return b

  def get_headers(self):
    return self.key_iv + self.cipher_iv

  def crypt(self, s):
    s = bytearray(s)
    for i in xrange(len(s)):
      s[i] ^= self.get_keystream_byte()
    return str(s)

def tryit(bdepth,ctype,height=480):
    width=640
    print 'trying',bdepth,ctype,height
    magic=[137,80,78,71,13,10,26,10,0,0,0,0xd,0x49,0x48,0x44,0x52,0,0,-1,-1,0,0,-1,-1,-1,-1,0,0,0,-1,-1,-1,-1,0,0,0,-1,-1,-1,-1,0,0,0,9,0x70,0x48,0x59,0x73]
    ihdr='49484452'.decode('hex') + pack('>I',width) + pack('>I',height)
    ihdr+=chr(bdepth)+chr(ctype)+'\x00\x00\x00'
    magic='89504E470D0A1A0A0000000D'.decode('hex')+ihdr+pack('>I',zlib.crc32(ihdr)&0xffffffff)+'00'.decode('hex')
    magic=map(ord,magic)
    
    #magic=[137, 80, 78, 71, 13, 10, 26, 10, 0, 0, 0, 13, 73, 72, 68, 82, 0, 0, 2, 128, 0, 0, 1, 224, 8, 2, 0, 0, 0, 0xba, 0xb3, 0x4b, 0xb3, 0,-1,-1,-1,0x49,0x44,0x41,0x54]
    ks=[]
    for i in range(20,len(magic)):
      if magic[i]!=-1:
        ks.append([i,ord(encdata[i])^magic[i]])
    mend='49454E44AE426082'.decode('hex')
    mend=map(ord,mend)
    for i in range(1,9)[::-1]:
      ks.append([len(encdata)-i,ord(encdata[-i])^mend[-i]])
    #print ks
    #print len(ks)
    
    key=[]
    '''
    c=LFSRCipher('\x00'*20,20,key_iv,cipher_iv)
    print c.crypt(encdata[:20]).encode('hex')
    exit()
    '''
    key_iv_stream = BitStream(key_iv)
    cipher_iv_stream = BitStream(cipher_iv)
    
    '''
    kiv=key_iv_stream.get_bits(20)
    civ=cipher_iv_stream.get_bits(20)
    for i in range(100):
      l = LFSR(i^kiv, civ, 20)
      for j in range(20):
        print l.get_bit(),
      print
    exit()
    '''
    for i in range(8):
      found=0
      print i
      kiv=key_iv_stream.get_bits(20)
      civ=cipher_iv_stream.get_bits(20)
      bits=[]
      for idx,k in ks:
        bits.append([idx,(k>>i)&1])
      tmp=[]
      for cand in range(2**20):
        l = LFSR(cand^kiv, civ, 20)
        ok=True
        pos=0
        j=0
        while pos<len(bits):
          cur=l.get_bit()
          if bits[pos][0]==j:
            if cur!=bits[pos][1]:
              ok=False
            pos+=1
          if not ok:
            break
          j+=1
        if ok:
          found+=1
          print i,cand
          tmp.append(cand)
      key.append(tmp)
      if found==0:
        return False
    print key
    return True

hh=0
while hh<480:
    hh+=10
    for ctype in [0,2,3,4,6]:
        if ctype==0:
            bb=[1,2,4,8,16]
        elif ctype==3:
            bb=[1,2,4,8]
        else:
            bb=[8,16]
        for bdepth in bb:
            if tryit(bdepth, ctype, hh):
                print 'good'
                exit()
    
    
