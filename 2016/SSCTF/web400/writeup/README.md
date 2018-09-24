github的一个授权问题，可以获得我们的头像和昵称等信息。这道题有幸看到了主办方尚未修复的“bug”，其实也就是提示了，howmp这个用户的昵称一开始就是`{{app.secret_key}}`
很容易想到修改昵称达到类似模板注入的方法，而且根据服务器返回的HTTP Header里面的`via`可以看出是python的什么框架（后来看到是flask）。然后就想着读文件了，先是普通的listdir，可以看到这个网站主要就是`ssctf.py`了。
接下来就是想办法读取文件内容，这里有很多限制，普通的open就会500错误。想起了HCTF2014的一道限制重重的python shell的题目，于是就找到了当时用的绕过方法
```
{{().__class__.__bases__[0].__subclasses__()[40]('ssctf.py').read()}}
```
ssctf.py代码中可以看到flag，而且其实可以直接不用绕过，猜到{{app.flagman}}也可以。