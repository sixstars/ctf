拿到一份pdf文件，用`pdfinfo`也就看出个作者姓名，没有什么其他有用的信息。

然后就开始联想题目的名字，速度数据是什么呢？想了很久也想不出来。

后来索性拿010editor跑了一下pdf的模板，发现有一些`0x20 0x09`的没套进模板。

于是猜测这是隐藏信息，制表符代表1，空格代表0，可以依次猜出txtFlag，然后用python简单的跑了一下。
```python
>>> ''.join([chr(int(i[:7].replace('\t','1').replace(' ','0'),2)) for i in open('misc2-ecac0a7e.pdf','rb').read().split('endobj ')[1:]])
'\x00txtFlag is SSCTF{6a6857ce76d4d6ce3b0e02b9e3738698}'
>>>
```
同时想起来自己看过《数据隐藏技术揭秘》，谈到过pdf的隐写方法，跑去图书馆借了一本，发现有现成的工具`wbstego.wbailer.com`可以直接提出flag。
