转贴自：<https://bbs.pediy.com/thread-223664.htm>

----

看了这篇帖子 <https://bbs.pediy.com/thread-223659.htm>

前人之述备矣，然在下仍觉细节尚缺，故有此文。

看了题目名字就知道这是32c3那道readme翻版。

32c3那道题是一个栈溢出，通过stack_chk_fail去调用fortify_fail。

当时的利用方法是控制栈上的参数，也就是argv和环境变量。特别注意要控制`LIBC_FATAL_STDERR_=1`让fortify_fail能够把输出作为stderr给我们。否则`fortify_fail`下层接的是`libc_message`，而`libc_message`调用的是`getenv`。

getenv就是从environ指针那里去找环境变量指针数组。

getenv如果发现这环境变量没设置，libc_message会syscall调用`open('/dev/tty')`，输出你是看不到的。

而34c3这道题的想法应该是源自于0ctf 2017里面的easiest printf（个人猜测）。

当时在0ctf结束后的irc里面，rpisec的人说到了一种非预期解法，就是改printf相关的两个函数指针，用自定义扩展%k调用shell。连dragon sector的人都很吃惊。

```
08:20 < itszn> Murmus: I used the hooks for printf for new char codes
08:20 < Redford> spq: discrete log on polynomial field
08:20 < its_> anyone has a writeup for the webshop?
08:20 < itszn> So I made %k give me a shell
08:20 < Gynvael> uhm
08:20 < Gynvael> printf has such an option?
08:20 < Gynvael> ^_-
08:20 < itszn> Yup
08:20 < Gynvael> TIL
08:20 < Murmus> TIL
08:21 < msm-> TIL
08:21 < Murmus> damn, that's awesome, I had no idea
08:21 < dude12312414_> lol
08:21 < WGH> Gynvael, Murmus: like WTFH4X (apparently) by overwrite vtable file stdout's FILE*
08:21 < itszn> There are two pointers to array of function pointers you have to set though
08:21 < itszn> So probably a little harder
08:21 < itszn> But first thing I thought of
```
这种精巧的利用来源于printf的一个功能：<https://www.gnu.org/software/libc/manual/html_node/Customizing-Printf.html#Customizing-Printf>

我不知道原帖作者是否仔细看了GNU的文档或者[printf的源代码](https://code.woboq.org/userspace/glibc/stdio-common/printf-parsemb.c.html#__parse_one_specmb)。

这里实际有两次RIP控制的机会，对应与printf的逻辑：首先是`printf_arginfo_table`，调用函数指针完成自定义spec的参数数目和类型的指定，后来才是对应的`printf_function_table`做真正的输出。

这里还有一点是，看完printf的代码你会知道，检查自定义spec是优先于printf自带的spec的。

于是ESPR他们应该是造了readme-revenge来结合上述两道题。

由于这道题是静态连接，又有`bss`段上的溢出，于是可以控制printf相关的函数指针和`libc_argv`。那么你就可以去构造%s对应的函数指针去控制RIP。

但是需要注意到`environ`指针是你覆盖不到的，他的位置在输入的上面。

所以说这种原帖作者所说的利用是存在问题的，你控制不了envivon啊？我不知道原帖作者是忘了、不知道还是故意没提（我希望是前两者）。在下第一时间就是因为这一点所以觉得这种思路不可用，去漫天找其他gadget。

实际上，217的同学也表示队友找了5个小时RCE的gadget找不到。
> 04:46 < david942j> _2can: yap.. it took my teammate 5hrs to try to do RCE (but fails as well)

是的，想要做这道题，需要撞大运，撞一个主办方帮你设置了环境变量`LIBC_FATAL_STDERR_=1`。

一个队友去撞了，于是成功get flag……真的是……哎。

如果你想要复现这个题目，要注意服务端把stderr导给stdout，并且把环境变量设好。

最后感谢原帖作者的分享。在下写这篇文章不是想批判原帖作者，只是认为有必要做一点细节的补充。因为个人认为，这些质量上乘的题目，好就好在引导我们去深入更加底层的程序运作和代码实现的细节。

希望能在看雪上看到更多的，经过自己辛勤探索、苦读代码、精心分析所得的干货。

PS:呼，不知不觉写了半个小时，不知道能混个精华么？:P
