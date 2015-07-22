```python
>>> from pwn import *
>>> from utils import *
>>> io = process('cat')
[+] Started program 'cat'
>>> io.sendline('0\x30 A\x41')
>>> io.recvline(False)
'00 AA'
>>> io.ext_interactive()
[*] Switching to extensive interactive mode
A\x410\x30
AA00
```