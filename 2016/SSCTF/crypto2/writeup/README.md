大坑爹题。
文件解压之后全是加密zip包，一开始完全不知道怎么办，只能看出有两个包比较大，有`pwd.zip`和`flag.zip`。
后来队友发现题目的提示中的start加了引号，于是用start做密码批量解压，虽然还是有crc错误。
但是不知道为什么队友用的是7zip，然后解出来的文件内容是乱码，于是我们想到用pkcrack攻击，等了了很久结果失败了。
后来我用某国产压缩软件批量解压试了一下，出来了一个1.txt，并且提示了下一个密码。这就很明确了，写脚本不断批量解压就可以了。
```python
import zipfile
import os
root = '.'
flag = 0
global flag

def check(zipfile):
	if len(zipfile.namelist()) > 1:
		return True
	return False


def dec(index):
	tmp = zipfile.ZipFile(index + '.zip')
	try:
		tmp.extract('1.txt', '.', pwd)
	except RuntimeError:
		pass
	except zipfile.BadZipfile:
		print index 
	else:
		print index
		newpwd = open('1.txt').read().replace('Next password is ','')
		print newpwd
		open('pwd.txt', 'w').write(newpwd)
		if check(tmp):
			tmp.extract(tmp.namelist()[1], '.', pwd)
			global flag
			flag += 1

		del(tmp)
		os.remove(index + '.zip')
		print '\nDelete ' + index + '.zip'
		return True
	return False

while True:
	if flag == 2:
		exit()
	pwd = open('pwd.txt').read()
	for i,j,k in os.walk('.'):
		for f in k:
			filename = os.path.splitext(f)
			if filename[1] == '.zip' and filename[0].isdigit():
				if dec(filename[0]) :
					break

```

出来`flag.zip`还是加密的，想必密码就在`pwd.zip`中了。解压`pwd.zip`可以得到一堆txt，其中有一个start.txt，然后用`grep -v "next" *.txt`找到终点。
因为有地方出现了分支，然而我不会DFS那些，就索性用grep从终点溯源。考虑到执行grep的方便，就写了个perl脚本：
```perl
#!/usr/bin/perl -w
use strict;
my $now = "376831";
while(1){
	my $next = `grep -l $now *.txt`;
	#print 'fuck!' if($next =~/"\n"/);
	my @now = split(/\./, $next);
	$now = $now[0];
	print $now.' ';
	exit if $now eq 'start'
}

```

跑一下`perl solve.pl > result` 就可以得到溯源之路。
然后在"collect comments"卡了好久。后来才知道zip包里面的文件有备注这种东西，简单看几个就可以发现有\t有空的，有空格。
于是猜想对应0和1，再用zipfile跑一次即可。
```python
import zipfile
from ctf import *
nodes = open('result').read().strip().split(' ')[::-1]
root = zipfile.ZipFile('pwd.zip')
ans = ''
for x in nodes:
  #print x
  c = root.getinfo(x.strip() + '.txt').comment
  if c == '\t':
    ans += '0'
  elif c == ' ':
    ans += '1'
  else :
    print 'no comment for %s' % (x)

print ans
print xor(unbits(ans),0xff)
```

