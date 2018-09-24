先下载备份文件index.php~，发现是一个被混淆过的php文件，找到个破解网站 http://zhaoyuanma.com/phpjm.php，破解后的源代码提示需要满足 `$test=$_GET['test']; $test=md5($test); if($test=='0')`

那么md5($test)什么时候会和'0'相等呢？

找到一篇解释 http://stackoverflow.com/questions/22140204/why-md5240610708-is-equal-to-md5qnkcdzo

了解到当使用=='0'做比较时，会将md5字符串转换成数字。那么只要找到能够被转换成0的md5字符串即可。由于240610708的md5值是`0e462097431906509019562988736854`，它可以代表一个浮点数0（因为0e代表科学计数法），那么它和0比较的时候就会相等，于是将240610708作为test的参数，可以获取flag。
