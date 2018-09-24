逆向 apk 发现 login 的时候，就是用 key.db 中存的 key 加密 username + passwd，然后和 flag.bin 对比。

于是查看 key.db：

```
SQLite version 3.8.10.2 2015-05-20 18:17:19
Enter ".help" for usage hints.
sqlite> .tables
key
sqlite> select * from key;
0|zctf2016
sqlite>
```

然后用 key 解密 flag.bin 后 reverse 得 `username + passwd = zctf{Notthis}`，
鉴于 username 默认为 zctf，猜测 passwd 为 `{Notthis`。

逆向 libJNIclass.so 发现，其用 passwd 解密了 top + bottom，top 为程序内一段常量，bottom 为 asserts 中的文件。
解密函数叫做 DES_Decrypt，然而自己 DES 解密得到的东西不对，动态调试（调试时需要 patch 掉 so 中的 ptrace，以及最好 patch 或者 hook 掉 java 中那个 3500ms 结束程序，否则我这里是总会在步过 DES Decrypt 时挂掉）或者写程序外部调用解密函数可以得到正确解密的结果。
解密后可以看到明显的 PNG 头，用 stegsolve 调一调即可见 flag。
