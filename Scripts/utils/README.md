# Utils For CTF

## Install

This repo is collections for some utils I may use.
And some features are inspired by [zio], as [pwntools] doesn't support.

As this is just a personal small tool, it doesn't support `pip install`.
If you'd like to import it anywhere, append the python's module search path.

For example, add the command below to `.bashrc/.zshrc`:

```bash
export PYTHONPATH="/path/to/directory/of/utils:$PYTHONPATH"
```

If you'd like to use another name for import, I suggest you to create a symbol link instead of directly renaming this file.
Then you can update this tool by simply executing `git pull`.

## Usage

1. This util will automatically export all functions in [pwntools]. So you can omit `from pwn import *` if you already use `from utils import *`.

1. Some functions / methods in [pwntools] are enhanced:

    * unhex: hex-strings with odd length are acceptable

    * tube.send, tube.sendline: automatically convert input data to string

1. Add some extra functions / methods for exp writing:

    * ljust / rjust: similar to str.ljust / str.rjust, but with length check

    * tube.sendlines: send multiple lines in one command

    * debug: run gdb for debugging

    * tube.ext_interactive: interactive shell with python style string supported

    * tube.b, tube.r, tube.c, tube.interrupt: short hand for command in gdb

1. Add some utils for calculation:

    * factor: integer factorization

    * gcd: calculate greatest common divisor

    * ext_euclid: extended Euclidean algorithm

    * rsa_decrypt: decrypt RSA encrypted message

1. Use `ext_interactive` to input unprintable chars：

    ```python
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

1. use `gdb` to debug：

    ```python
    >>> from utils import *
    >>> io = debug('cat')
    [x] Starting program '/usr/local/bin/gdb' argv=['gdb', 'cat']    [+] Starting program '/usr/local/bin/gdb' argv=['gdb', 'cat'] : Done
    >>> # io.b('main') <=> io.sendline('b main')
    >>> # io.b(0x08040000) <=> io.sendline('b * 0x08040000')
    >>> # io.c() <=> io.sendline('c')
    >>> io.r() # <=> io.sendline('r')
    >>> io.ext_interactive()
    [*] Switching to extensive interactive mode    GNU gdb (GDB) 7.9    ...
    Reading symbols from cat...(no debugging symbols found)...done.
    gdb-peda$ gdb$ Starting program: /bin/cat    0\x30\t\x41A    00	AA
    ### Pressed ctrl+c here in order to interrupt the running program ###
    Program received signal SIGINT, Interrupt.
    ...
    Stopped reason: SIGINT    0x00007ffff7b003a0 in read () from /lib/x86_64-linux-gnu/libc.so.6
    gdb$ i prog        Using the running image of child process 6695.    Program stopped at 0x7ffff7b003a0.    It stopped with signal SIGINT, Interrupt.    Type "info stack" or "info registers" for more information.
    gdb$ c!
    ### input c! <=> exit interactive mode and run io.c() ###
    Continuing.
    >>> io.sendline('A\x410\x30')    >>> io.recvline(False)    'AA00'    ```

## LICENSE

GPL

[zio]: https://github.com/zTrix/zio
[pwntools]: https://github.com/Gallopsled/pwntools
