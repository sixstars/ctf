1. 使用`ext_interactive`交互输入不可见字符：

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

2. 使用`gdb`调试程序：

	```python
	>>> from pwn import *
	>>> from utils import *
	>>> io = debug('cat')
	[x] Starting program '/usr/local/bin/gdb' argv=['gdb', 'cat'] [+] Starting program '/usr/local/bin/gdb' argv=['gdb', 'cat'] : Done
	>>> # io.b('main') <=> io.sendline('b main')
	>>> # io.b(0x08040000) <=> io.sendline('b * 0x08040000')
	>>> # io.c() <=> io.sendline('c')
	>>> io.r() # <=> io.sendline('r')
	>>> io.ext_interactive()
	[*] Switching to extensive interactive mode	GNU gdb (GDB) 7.9	...
	Reading symbols from cat...(no debugging symbols found)...done.
	gdb-peda$ gdb$ Starting program: /bin/cat 	0\x30\t\x41A	00	AA
	### Pressed ctrl+c here in order to interrupt the running program ###
	Program received signal SIGINT, Interrupt.
	...
	Stopped reason: SIGINT	0x00007ffff7b003a0 in read () from /lib/x86_64-linux-gnu/libc.so.6
	gdb$ i prog		Using the running image of child process 6695.	Program stopped at 0x7ffff7b003a0.	It stopped with signal SIGINT, Interrupt.	Type "info stack" or "info registers" for more information.
	gdb$ c!
	### input c! <=> exit interactive mode and run io.c() ###
	Continuing.
	>>> io.sendline('A\x410\x30')	>>> io.recvline(False)	'AA00'	```