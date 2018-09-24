一道Windows逆向题，首先Win10直接跑跑不起来，然后调了个兼容性模式跑起来了，但是程序还是会莫名其妙地挂。

IDA载入后发现是字符串比较，主要函数如下：

```c
int __cdecl key(int a1)
{
  int result; // eax@1
  int v2; // ST04_4@5
  int v3; // [sp+4h] [bp-14h]@1
  signed int i; // [sp+8h] [bp-10h]@1

  result = *(_DWORD *)(a1 + 4);
  v3 = *(_DWORD *)(result + 8);
  for ( i = 0; i < 15; ++i )
  {
    if ( i + (signed __int16)(*(_BYTE *)(*(_DWORD *)(*(_DWORD *)(a1 + 8) + 16) + i) ^ *(_BYTE *)(i + v3) & 0xF) != *(_DWORD *)(**(_DWORD **)(a1 + 4) + 4 * i)
      || (signed __int16)(*(_BYTE *)(*(_DWORD *)(*(_DWORD *)(a1 + 8) + 20) + i) ^ (unsigned __int16)((signed int)*(_BYTE *)(i + v3) >> 4))
       - i != *(_DWORD *)(*(_DWORD *)(*(_DWORD *)(a1 + 4) + 4) + 4 * i) )
    {
      (*(void (__cdecl **)(_DWORD))(*(_DWORD *)a1 + 12))(*(_DWORD *)(*(_DWORD *)(a1 + 8) + 16));
      v2 = *(_DWORD *)(*(_DWORD *)(a1 + 8) + 16);
      (*(void (__stdcall **)(_DWORD))(*(_DWORD *)a1 + 12))(0);
      exit(0);
    }
    result = (*(int (__cdecl **)(_DWORD))(*(_DWORD *)a1 + 12))(*(_DWORD *)(*(_DWORD *)(a1 + 8) + 20));
  }
  return result;
}
```

可以看到我们要的就是if条件中||分隔计算的两个布尔表达式为False。动态调试或者从上一层函数的
```c
  v4 = &unk_404054;
  v5 = &unk_404018;
```
可以找到我们的目标字符串，然后异或的字符串实际上就是`sorry,please try again!\n`和`Congratulation! you got a right flag!\n`。

这道题奇怪的地方在于，异或后还有跟索引值的加减操作，但是发现这样做会有不可见字符？然后我再某一次OD跟的时候不知道为啥脑子短路觉得是IDA翻译反了，就把+-颠倒了一下，竟然就出来了：

```python
>>> dest1       = 'retst$yg^^f\\\x17je'
>>> dest1
'retst$yg^^f\\\x17je'
>>> print dest1
retst$yg^^f\je
>>> dest1
'retst$yg^^f\\\x17je'
>>> dest2 = '@jkculwywo\x81ytz0'
>>> len(dest1)
15
>>> len(dest2)
15
>>> xor2 = "Congratulation! you got a right flag!\n"
>>> xor1 = "sorry,please try again!\n"
>>> len(xor1)
>>> l = [(ord(dest1[i]) + i)^ord(xor1[i]) for i in range(15)]
>>> h = [(ord(dest2[i]) - i)^ord(xor2[i]) for i in range(15)]
>>> h
[3, 6, 7, 7, 3, 6, 5, 7, 3, 7, 3, 7, 7, 3, 3]
>>> l
[1, 9, 4, 4, 1, 5, 15, 2, 3, 6, 3, 2, 3, 3, 1]
>>> [chr(h[i]*16 + l[i]) for i in range(15)]
['1', 'i', 't', 't', '1', 'e', '_', 'r', '3', 'v', '3', 'r', 's', '3', '1']
>>> print ''.join([chr(h[i]*16 + l[i]) for i in range(15)])
1itt1e_r3v3rs31

```
