# tjctf2017

## Windows逆向1

运行返回一个二维码，扫描告知需要知道`flag.dll`的函数调用顺序。

用IDA载入就知道里面有两个东西0和1，于是猜测是要记录主程序调用0和1的过程。然后发现0和1指向同一个地址，并且只有一个光的`retn`。

然后去看主程序，通过IDA可以很快找到入口处加载`flag.dll`的逻辑。

```asm
.text:00A0A225                 push    offset aFlag_dll ; "Flag.dll"
.text:00A0A22A                 call    ds:LoadLibraryA
.text:00A0A230                 mov     edi, eax
.text:00A0A232                 push    offset a_0      ; "_0"
.text:00A0A237                 push    edi
.text:00A0A238                 call    ds:GetProcAddress
.text:00A0A23E                 push    offset a_1      ; "_1"
.text:00A0A243                 push    edi
.text:00A0A244                 mov     off_A3CD6C, eax
.text:00A0A249                 call    ds:GetProcAddress
.text:00A0A24F                 lea     ecx, [ebp-28C88h]
.text:00A0A255                 mov     dword_A3CD68, eax
```

说是逆向，实际上考察动态调试技巧。只要在第二次`GetProcAddress`的时候修改eax即可分离0和1。

分离完0和1就是断点的trace问题了，找了很久发现python灰帽已经讲的很清楚了。

## Windows逆向2
VMP壳，动态调试找到接输入的逻辑。然后单步跟踪可以发现用`tj{maybe_the_time_isn't_right}`作为key更改了`0x401200`开始的一段代码。

观察`0x401200`发现是取输入的3个字符，然后经过一个奇怪的hash，和已有的一张表进行比对，flag长度为3\*17=51。

于是写程序暴力破解即可。见 <https://github.com/elnx/0x9BE74448>

## Python Opcode
魔改版的python，更改了opcode，并删除了`dis`需要的`opcode.py`。

写一些代码进行对比即可找出对应关系，修改原版`opecode.py`，注意一些opcode出现多次的问题。

最终`opcode.py`见<https://gist.github.com/elnx/00cd7b80781ba39471695fd5efca38f1>

用`marshal`和`dis`即可翻译出汇编，见<https://gist.github.com/elnx/57905c8457383f8ac225b6a9570db162>



