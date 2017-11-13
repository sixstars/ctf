# sms

32位程序，没canary没PIE。

漏洞也非常明显，是只检查了函数指针数组的上界没有检查下界，于是输入负数就可以调用got表上的函数。

比赛中未做出。尝试了很多函数，都拿不到很好的控制权。

赛后阅读了TheRomanXpl0it的writuep <https://theromanxpl0it.github.io/ctf_codeblue2017/secretmailerservice/>

其利用的核心的就是用setbuf改掉`/dev/null`的缓冲区，配合参数改好可以改到栈上，于是就回到stack smash。

但dp1的做法略微有些繁琐，还跳回`Main()`。实际没有必要，用ROP即可。

流程为：用puts泄漏got表，拿到libc，通过两次pop一次ret跳到`readN`上，然后随便写一块可写区域，然后通过3次pop跳到leave_ret。其中第三次pop为pop ebp，提前放好buf占位，配合leave，栈会迁移到我们的buf上。
