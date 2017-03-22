## py

利用`marshal.loads`我们人肉扣出encrypt字节码，并根据常量发现了pip里有rotor模块，对着字节码进行了如下脑洞：
```
\x99\x01\x00    load consts   key_a="!@#$%^&*"
\x68\x01\x00    store

\x99\x02\x00    load  consts  key_b="abcdefgh"
\x68\x02\x00    store

\x99\x03\x00    load  consts  key_c="<>{}:""
\x68\x03\x00    store

\x61\x01\x00    load_f key_a
\x99\x04\x00    load consts 4
\x46 *          key_a * 4

\x99\x05\x00    load consts |
\x27 +          key_a * 4 + "|"

\x61\x02\x00    load_f key_b
\x61\x01\x00    load_f key_a
\x27 +

\x61\x03\x00    load_f key_c
\x27 +          key_b + key_a + key_c

\x99\x06\x00    load consts 2
\x46 *          (key_b + key_a + key_c) * 2
\x27 +          key_a * 4 + "|" + (key_b + key_a + key_c) * 2

\x99\x05\x00    load consts |
\x27 +          key_a * 4 + "|" + (key_b + key_a + key_c) * 2 + "|"

\x61\x02\x00    load_f key_b
\x99\x06\x00    load consts 2
\x46 *          key_b * 2
\x27 +          key_a * 4 + "|" + (key_b + key_a + key_c) * 2 + "|" + key_b * 2

\x99\x07\x00    load consts "EOF"
\x27 +          key_a * 4 + "|" + (key_b + key_a + key_c) * 2 + "|" + key_b * 2 + "EOF"

\x68\x04\x00    store secret = key_a * 4 + "|" + (key_b + key_a + key_c) * 2 + "|" + key_b * 2 + "EOF"
\x9b\x00\x00    IMPORT rotor
\x60\x01\x00    PUSH rotor.rotor

\x61\x04\x00    load_f secret
\x83\x01\x00    CALL # rotor.rotor(secret)

\x68\x05\x00    store rot = rotor.rotor(secret)
\x61\x05\x00    load_f rot
\x60\x02\x00    PUSH rot.encrypt

\x61\x00\x00    load_f data
\x83\x01\x00    CALL # rot.encrypt(data)

\x53            return
```

其实`\x27`很容易就猜出来是字符串拼接`+`，但是`\x46`我们一开始猜测是SLICE+1, SLICE+2 (即string[x:]和string[:x])折腾了好久，后来才脑洞出来字符串操作还有一个`*`....
于是就出来了，把secret扔进去rotor模块在decrypt一下就好。
