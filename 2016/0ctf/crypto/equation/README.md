#equation crypto 2
这道题给出一张图片，内容是RSA私钥的后半部分，根据题意要恢复出整个私钥，也就是找到原来的p和q。
这到题首先google了好久，结果走了弯路，找到了以前plaid ctf的一道题目，理论依据是一篇论文，讲的是随机撤掉私钥中70%左右的bit都可以恢复。
后来仔细看了一些那道题的writeup，发现有几个方程可以用:`http://mslc.ctf.su/wp/plaidctf-2014-rsa-writeup/`
自己人肉decode一下私钥可以得到dp和dq，然后找帖子中的代码，遍历kp和kq（这里认为e是65537），就可以算出pq，而且算q的时候可以根据私钥中残缺的q来判断。
然后用rsatool就可以恢复出整个私钥。