#!/usr/bin/env python3
from binascii import hexlify
from binascii import unhexlify
import logging
import sys
import os

from curve25519 import Private, Public
import nacl.secret
import hmac
import hashlib

from pwn import *

context.log_level='debug'

sk=Private()
mypk=b'\xed\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x7f'
pk=Public(mypk)
myshare=sk.get_shared_key(pk)

def getmac(myn):
    c = remote('mitm.ctfcompetition.com', 1337)
    c.sendline('c')
    pk = c.recvline()
    n0 = c.recvline()
    c.sendline(hexlify(mypk))
    c.sendline(myn)
    mac = c.recvline()
    c.close()
    return mac

'''
cli = remote('mitm.ctfcompetition.com', 1337)
cli.sendline('c')
pkc = cli.recvline()
nc = cli.recvline()
mac = getmac(nc)
cli.sendline(hexlify(mypk))
cli.sendline(mac)
'''
secbox = nacl.secret.SecretBox(myshare)

ser = remote('mitm.ctfcompetition.com', 1337)
ser.sendline('s')
pkc = ser.recvline()
nc = ser.recvline()
mac = getmac(nc)
ser.sendline(hexlify(mypk))
ser.sendline(hexlify(b'\x00'*32))
ser.recvline()
ser.send(mac)

msg = ser.recvline().strip()
print(secbox.decrypt(unhexlify(msg)))
ser.sendline(hexlify(secbox.encrypt(b'getflag')))
msg = ser.recvline().strip()
print(secbox.decrypt(unhexlify(msg)))
ser.interactive()

def ReadLine(reader):
  data = b''
  while not data.endswith(b'\n'):
    cur = reader.read(1)
    data += cur
    if cur == b'':
      return data
  return data[:-1]


def WriteLine(writer, msg):
  writer.write(msg + b'\n')
  writer.flush()


def ReadBin(reader):
  return unhexlify(ReadLine(reader))


def WriteBin(writer, data):
  WriteLine(writer, hexlify(data))


def ComputeProof(key, data):
  return hmac.new(key, data, digestmod=hashlib.sha256).digest()


def VerifyProof(key, data, proof):
  return hmac.compare_digest(ComputeProof(key, data), proof)


def Handshake(password, reader, writer):
  myPrivateKey = Private()
  myNonce = os.urandom(32)

  WriteBin(writer, myPrivateKey.get_public().serialize())
  WriteBin(writer, myNonce)

  theirPublicKey = ReadBin(reader)
  theirNonce = ReadBin(reader)

  if myNonce == theirNonce:
    return None
  if theirPublicKey in (b'\x00'*32, b'\x01' + (b'\x00' * 31)):
    return None

  theirPublicKey = Public(theirPublicKey)

  sharedKey = myPrivateKey.get_shared_key(theirPublicKey)
  myProof = ComputeProof(sharedKey, theirNonce + password)

  WriteBin(writer, myProof)
  theirProof = ReadBin(reader)

  if not VerifyProof(sharedKey, myNonce + password, theirProof):
    return None

  return sharedKey


def Server(password, flag, reader, writer):
  sharedKey = Handshake(password, reader, writer)
  if sharedKey is None:
    WriteLine(writer, b'Error: nope.')
    return 1

  mySecretBox = nacl.secret.SecretBox(sharedKey)
  WriteBin(writer, mySecretBox.encrypt(b"AUTHENTICATED"))

  while 1:
    cmd = mySecretBox.decrypt(ReadBin(reader))
    if cmd == b'help':
      rsp = b'help|exit|whoami|getflag'
    elif cmd == b'exit':
      return 0
    elif cmd == b'whoami':
      rsp = b'root'
    elif cmd == b'getflag':
      rsp = flag
    else:
      return 1
    WriteBin(writer, mySecretBox.encrypt(rsp))


def Client(password, reader, writer):
  sharedKey = Handshake(password, reader, writer)
  if sharedKey is None:
    WriteLine(writer, b'Error: nope.')
    return 1

  mySecretBox = nacl.secret.SecretBox(sharedKey)
  line = mySecretBox.decrypt(ReadBin(reader))
  if line != b"AUTHENTICATED":
    WriteLine(writer, b'Error: nope.')
    return 1

  WriteBin(writer, mySecretBox.encrypt(b"whoami"))
  line = mySecretBox.decrypt(ReadBin(reader))

  if line != b'root':
    return 1

  WriteBin(writer, mySecretBox.encrypt(b"exit"))
  return 0


def Challenge(password, flag, reader, writer):
  try:
    server_or_client = ReadLine(reader)
    is_server = server_or_client[0] in b'sS'
    is_client = server_or_client[0] in b'cC'

    if is_server:
      return Server(password, flag, reader, writer)
    elif is_client:
      return Client(password, reader, writer)
    else:
      WriteLine(writer, b'Error: Select if you want to speak to the (s)erver or (c)lient.')
      return 1
  except Exception as e:
    WriteLine(writer, b'Error')
    return 1

