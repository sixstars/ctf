非常精美的一道题目。

整个程序不断read获取输入，直到read失败。

然后把我们的输入打碎为一个个byte，中间插入15个nop，在头尾加上一些预设的指令，开辟新的内存放入。

之后读取自身的`/proc/self/maps`，用`munmap`删除自身各个段，只保留了存放输入的一段和栈，最后跳到输入段开头开始执行。

于是就考察写shellcode。

思路就是先找到所有可用的指令，然后找能够做修改内存操作的指令。另外，结尾处有syscall可用，还需要搜索特征来定位这个syscall，方便最后ret。

最重要的两个指令是scas和stos，scas负责搜索syscall，而stos负责修改栈上的东西。那么execve就可以实现了。

还有一个细节是由于shutdown了write，需要做一次tcp reverse shell。
