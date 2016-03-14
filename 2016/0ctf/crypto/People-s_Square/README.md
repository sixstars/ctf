## People's Square

看了下程序逻辑，发现实现了一个4轮的AES，而且在output.txt中我们有大量的稍微不同的输入与加密结果。网上搜了下AES Differential在某篇论文中发现了SQUARE ATTACK跟我们有的输入相符，然后在github上搜到[相关代码](https://github.com/Yogitha6/AES_SquareAttack_4rounds)，根据256个连续密文可以得到可能的key集合，多弄几次取交集得到key为`['17', '4a', '22', '14', '40', '35', '64', '75', 'dc', 'e3', 'a0', '37', 'a3', '17', 'ed', '4b']`。另外似乎那个代码里面的`rijndael-alg-fst.o`不支持4轮，稍微修改下后成功解密出flag为`0CTF{~R0MAN_l0VES_B10CK_C1PHER~}`
