### 尝试

原源代码：

```python
(lambda __g, __y: [[[[[[[(fin.close(), [[(lambda __items, __after, __sentinel: __y(lambda __this: lambda: (lambda __i: [(ss.append(c), (sss.append(0), __this())[1])[1] for __g['c'] in [(__i)]][0] if __i is not __sentinel else __after())(next(__items, __sentinel)))())(iter(s), lambda: [[(lambda __items, __after, __sentinel: __y(lambda __this: lambda: (lambda __i: [(lambda __value: [__this() for __g['sssss'] in [((lambda __ret: __g['sssss'] + __value if __ret is NotImplemented else __ret)(getattr(__g['sssss'], '__iadd__', lambda other: NotImplemented)(__value)))]][0])(chr(c)) for __g['c'] in [(__i)]][0] if __i is not __sentinel else __after())(next(__items, __sentinel)))())(iter(ssss), lambda: [(fout.write(sssss), (fout.close(), None)[1])[1] for __g['fout'] in [(open('flag.enc', 'wb+'))]][0], []) for __g['sssss'] in [('')]][0] for __g['ssss'] in [(encode(ss, sss))]][0], []) for __g['sss'] in [([])]][0] for __g['ss'] in [([])]][0])[1] for __g['s'] in [(fin.read().strip())]][0] for __g['fin'] in [(open('flag.txt', 'r'))]][0] for __g['encode'], encode.__name__ in [(lambda data, buf: (lambda __l: [[(lambda __items, __after, __sentinel: __y(lambda __this: lambda: (lambda __i: [[__this() for __l['data'][__l['i']] in [((table.index(__l['data'][__l['i']]) + 1))]][0] for __l['i'] in [(__i)]][0] if __i is not __sentinel else __after())(next(__items, __sentinel)))())(iter(xrange(__l['_len'])), lambda: (lambda __items, __after, __sentinel: __y(lambda __this: lambda: (lambda __i: [[[__this() for __l['buf'] in [(setbit(__l['buf'], __l['i'], getbit(__l['data'], __l['j'])))]][0] for __l['j'] in [((((__l['i'] / 6) * 8) + (__l['i'] % 6)))]][0] for __l['i'] in [(__i)]][0] if __i is not __sentinel else __after())(next(__items, __sentinel)))())(iter(xrange((__l['_len'] * 6))), lambda: __l['buf'], []), []) for __l['_len'] in [(len(__l['data']))]][0] for __l['data'], __l['buf'] in [(data, buf)]][0])({}), 'encode')]][0] for __g['getbit'], getbit.__name__ in [(lambda p, pos: (lambda __l: [[[((__l['p'][__l['cpos']] >> __l['bpos']) & 1) for __l['bpos'] in [((__l['pos'] % 8))]][0] for __l['cpos'] in [((__l['pos'] / 8))]][0] for __l['p'], __l['pos'] in [(p, pos)]][0])({}), 'getbit')]][0] for __g['setbit'], setbit.__name__ in [(lambda p, pos, value: (lambda __l: [[[(lambda __target, __slice, __value: [(lambda __target, __slice, __value: [__l['p'] for __target[__slice] in [((lambda __old: (lambda __ret: __old | __value if __ret is NotImplemented else __ret)(getattr(__old, '__ior__', lambda other: NotImplemented)(__value)))(__target[__slice]))]][0])(__l['p'], __l['cpos'], (__l['value'] << __l['bpos'])) for __target[__slice] in [((lambda __old: (lambda __ret: __old & __value if __ret is NotImplemented else __ret)(getattr(__old, '__iand__', lambda other: NotImplemented)(__value)))(__target[__slice]))]][0])(__l['p'], __l['cpos'], (~(1 << __l['bpos']))) for __l['bpos'] in [((__l['pos'] % 8))]][0] for __l['cpos'] in [((__l['pos'] / 8))]][0] for __l['p'], __l['pos'], __l['value'] in [(p, pos, value)]][0])({}), 'setbit')]][0] for __g['table'] in [(string.printable.strip())]][0] for __g['string'] in [(__import__('string', __g, __g))]][0])(globals(), (lambda f: (lambda x: x(x))(lambda y: f(lambda: y(y)()))))
```

一大堆lambda...嗯，其实这题还是很简单的...    

在本地尝试执行，并查看globals()，得

```python
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 1, in <lambda>
IOError: [Errno 2] No such file or directory: 'flag.txt'
>>> globals()
{'string': <module 'string' from 'D:\Python27\lib\string.pyc'>, '__builtins__': <module '__builtin__' (built-in)>, '__package__': None, 'i': 654, 'table': '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', 'encode': <function encode at 0x02836C30>, '__name__': '__main__', 'getbit': <function getbit at 0x028364B0>, '__doc__': None, 'setbit': <function setbit at 0x02815E30>}
```

也就是import string，并生成了encode(), getbit(), setbit()的函数，还有一个table     
下面还是先介绍下背景知识吧....    

### 函数式编程与lambda运算

这个程序跟函数式编程还是有一定关系的，当然不会也能做...    
下面就是这个.py的主要trick     

#### 等量代换(实现where语句，scope内赋值)

不妨先看下这样的例子：    
`[y for y in [1]] == [1]`

再看个复杂点的

```python
[x for x in [range(3)]] == [x for x in [[0, 1, 2]]] == [ [0,1,2] ]
```

如果把最外层的方括号看成一个scope，也就是如同C语言里的{}所起的作用一样，那么这句话就是一个等量代换，把这句话变形一下易于理解，即：

```
[
	x
	for x in [range(3)]
]
```

去掉in，得

```
[
	x
	for x = range(3)
]
```

把最外层[]理解成c语言的scope

```
{
	x = range(3)
	返回 x
}
```

求值得

```
{
	[0, 1, 2]
}
```

把scope变回来，即得`[ [0,1,2] ]`
换句话，我们得到两个等量代换式：

`[blahblah(x) for x in [y] ] == [blahblah(x) where x = y]`
`[blahblah(x) for x in [[y]][0] ] == [blahblah(x) where x = y]`

这样相当于haskell的where语句    

也就是说，可以用这种形式实现在scope内的赋值操作，在scope内把x赋值为y     
比如说，要想得到`[(0, 0)]`我们可以这样写：     
`[(x, y) for x in [0] for y in [[0]][0]] == [(0, 0)]`

### lambda calculus beta规约（实现let语句）

以下是lambda calculus的beta规约定理的例子：

```python
(lambda j: j*2)(3) == (3*2) == 6
```

如果把lambda运算内部视为一个scope，那么就相当于

```
lambda:
	let j = 3:
		return j*2
```


#### 开始逆向

trick讲完了，就可以粗粗整理下代码了，加些赋值符号：

```python
(lambda __g, __y: [[[[[[[(fin.close(), [[(lambda __items, __after, __sentinel: __y(lambda __this: lambda:

(lambda __i: [(ss.append(c), (sss.append(0), __this())[1])[1]
for __g['c'] in [(__i)]][0] if __i is not __sentinel else __after())

(next(__items, __sentinel)))())(iter(s), lambda: [[(lambda __items, __after, __sentinel: __y(lambda __this: lambda: (lambda __i: [(lambda __value: [__this() for __g['sssss'] in [((lambda __ret: __g['sssss'] + __value if __ret is NotImplemented else __ret)(getattr(__g['sssss'], '__iadd__', lambda other: NotImplemented)(__value)))]][0])(chr(c)) for __g['c'] in [(__i)]][0] if __i is not __sentinel else __after())(next(__items, __sentinel)))())(iter(ssss), lambda: [(fout.write(sssss), (fout.close(), None)[1])[1] for __g['fout'] in [(open('flag.enc', 'wb+'))]][0], [])

for __g['sssss'] in [('')]][0]
for __g['ssss'] in [(encode(ss, sss))]][0], [])
for __g['sss'] in [([])]][0]
for __g['ss'] in [([])]

][0])[1]

for __g['s'] in [(fin.read().strip())]][0]

for __g['fin'] in [(open('flag.txt', 'r'))]][0]

for __g['encode'], encode.__name__ in [

(lambda data, buf:
  (lambda __items, __after, __sentinel:
    __y(lambda __this: lambda:
      (lambda __i:
        [data['i'] = ((table.index(data['i']) + 1))
        if __i is not __sentinel else __after())(next(__items, __sentinel)))())(iter(xrange(__l['_len'])),

        lambda: (lambda __items, __after, __sentinel:
          __y(lambda __this: lambda: (lambda __i: [[[

          __this() for __l['buf'] in [(
             j=(i / 6) * 8 + (i % 6)
             setbit(buf, i, getbit(data, j))

              if __i is not __sentinel else __after())(next(__items, __sentinel)))())

        (iter(xrange((__l['_len'] * 6))), lambda: __l['buf'], []), []) for __l['_len'] in [(len(__l['data']))] )

]][0]

for __g['getbit'], getbit.__name__ in [(lambda p, pos: (lambda __l: [[[((__l['p'][__l['cpos']] >> __l['bpos']) & 1) for __l['bpos'] in [((__l['pos'] % 8))]][0] for __l['cpos'] in [((__l['pos'] / 8))]][0] for __l['p'], __l['pos'] in [(p, pos)]][0])({}), 'getbit')]][0]

 for __g['setbit'], setbit.__name__ in [(lambda p, pos, value: (lambda __l: [[[(lambda __target, __slice, __value: [(lambda __target, __slice, __value: [__l['p'] for __target[__slice] in [((lambda __old: (lambda __ret: __old | __value if __ret is NotImplemented else __ret)(getattr(__old, '__ior__', lambda other: NotImplemented)(__value)))(__target[__slice]))]][0])(__l['p'], __l['cpos'], (__l['value'] << __l['bpos'])) for __target[__slice] in [((lambda __old: (lambda __ret: __old & __value if __ret is NotImplemented else __ret)(getattr(__old, '__iand__', lambda other: NotImplemented)(__value)))(__target[__slice]))]][0])(__l['p'], __l['cpos'], (~(1 << __l['bpos']))) for __l['bpos'] in [((__l['pos'] % 8))]][0] for __l['cpos'] in [((__l['pos'] / 8))]][0] for __l['p'], __l['pos'], __l['value'] in [(p, pos, value)]][0])({}), 'setbit')]][0]

 for __g['table'] in [(string.printable.strip())]][0] for __g['string'] in [(__import__('string', __g, __g))]][0])(globals(), (lambda f: (lambda x: x(x))(lambda y: f(lambda: y(y)()))))

```

核心部分我又整理了一次：

```python
[(fout.write(sssss), (fout.close(), None)[1])[1] for __g['fout'] in [(open('flag.enc', 'wb+'))]][0], []) for __g['sssss'] in [('')]][0] for __g['ssss'] in [(encode(ss, sss))]][0], []) for __g['sss'] in [([])]][0] for __g['ss'] in [([])]][0])[1] for __g['s'] in [(fin.read().strip())]][0] for __g['fin'] in [(open('flag.txt', 'r'))]][0] for __g['encode'], encode.__name__ in [
(lambda data, buf: (lambda __l: [[
  (lambda __items, __after, __sentinel: __y(
    lambda __this: lambda:
      (lambda __i: [[__this() for __l['data'][__l['i']] in [((table.index(__l['data'][__l['i']]) + 1))]][0] for __l['i'] in [(__i)]][0] if __i is not __sentinel else __after())(next(__items, __sentinel)))())(iter(xrange(__l['_len'])), lambda: (lambda __items, __after, __sentinel: __y(lambda __this: lambda: (lambda __i: [[[__this()
        for __l['buf'] in [(
          setbit(__l['buf'], __l['i'], getbit(__l['data'], __l['j'])))]][0]
            for __l['j'] in [((((__l['i'] / 6) * 8) + (__l['i'] % 6)))]][0]
            for __l['i'] in [(__i)]][0] if __i is not __sentinel else __after())(next(__items, __sentinel)))())(iter(xrange((__l['_len'] * 6))), lambda: __l['buf'], []), []) for __l['_len'] in [(len(__l['data']))]][0]

            for __l['data'], __l['buf'] in [(data, buf)]][0])({}), 'encode')]][0]
```

仔细看看，核心部分也就几句话：
```python
[data['i'] = ((table.index(data['i']) + 1))
__this() for __l['buf'] in [(
             j=(i / 6) * 8 + (i % 6)
             setbit(buf, i, getbit(data, j))

              if __i is not __sentinel else __after())(next(__items, __sentinel)))())

        (iter(xrange((__l['_len'] * 6)))

 for __g['table'] in [(string.printable.strip())]][0] for __g['string'] in [(__import__('string', __g, __g))]][0])(globals(), (lambda f: (lambda x: x(x))(lambda y: f(lambda: y(y)()))))
```

其中`__g[xxxxx]`就是全局变量，`__l[xxx]`就是局部变量

那么加密方式就出来了，把原字符在table的index+1后，把后6位保存到文件里      
（其实这里由于我懒得看setbit，getbit所以搞反了字节序，
后来把aaaaaaaaaaaa写入flag.txt用这个程序加密后仔细逐位对比后才发现- -||）

由于`6*4==3*8`，我就每3字节一起decode      
decode3b函数：

```python
def tobin(b):
	ret=''
	for i in [128,64,32,16,8,4,2,1]:
		ret+='1' if b&i else '0'
	return ret

def decode3b(s):
    a=s>>16
    b=(s>>8) & 0xFF
    c=s & 0xff
    sa=tobin(a)
    sb=tobin(b)
    sc=tobin(c)
    return table[int(sa[2:],2)]+table[int(sb[4:]+sa[:2],2)]+table[int(sc[6:]+sb[:4],2)]+table[int(sc[:6],2)]

>>> a=open('flag.enc','rb')
>>> a=a.read()
>>> s=''
>>> for i in xrange(0, len(a), 3):
...     s+=decode3b(int(a[i:i+3].encode('hex'), 16))
...
>>> s
'yedugr1ofbm2o4epQz8i1op2tpkxft1nf344t000000000000000'
>>> s=''.join(map(lambda c: table[(table.index(c)+63)%64], s))
'xdctfq0neal1n3doPy7h0no1sojwes0me233s"""""""""""""""'
```

由于只保留了最后6位，所以在table里的index大于64的特殊字符是没有的，要手动（脑）补上第7位，
查table+64可知`'q'->'{', 'o'->'_'`等等....
得：
`xdctf{0ne-l1n3d_Py7h0n_1s_@wes0me233}`
