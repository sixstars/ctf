这题很明显在strcpy的时候会有溢出，可以直接覆盖到返回地址，然后`checksec`可发现栈是可以执行的，于是乎直接执行shellcode即可。

将shellcode放在栈中后，我们需要定位其地址，最简单的方法当然莫过于用一个超长的NOP，然后大概定位一下就好，这里既然是平常练习，我们还是采取精确定位的方式。

因为需要在参数中不可见字符，字符串又较长，所以直接在shell下执行可能不是很方便，于是乎我们用Python来执行execve调用。

接下来，我们实现一个泄露地址的程序[leak.cpp](leak.cpp)，通过`printf("%p\n", argv[1]);`输出第一个参数的地址，然后为了保证我们在执行leak和narnia2的时候栈是一样的，我们首先看下栈的分布：

|   Stack bottom   |
|:----------------:|
| ebp before main  |
| ret addr of main |
|     int argc     |
|   char *argv[]   |
|   char *env[]    |
|     (unknown)    |
| pointer to arg 1 |
| pointer to arg 2 |
|       ...        |
| pointer to arg n |
|       null       |
| pointer to env 1 |
| pointer to env 2 |
|       ...        |
| pointer to env m |
|       null       |
|     (unknown)    |
|    argument 1    |
|    argument 2    |
|       ...        |
|    argument n    |
|  environment 1   |
|  environment 2   |
|       ...        |
|  environment m   |
|   binary name    |
|       null       |
|       null       |
|    stack top     |

于是乎，我们应该保证环境变量、参数的个数、长度都一样，这里关键就是把`argument 2`的长度始终补到一个定值即可。然后，还要注意的就是`binary name`，用execve执行的时候，这个就是execve的第一个参数的值，于是乎，保持这个长度一定最简单的办法就是建立一个临时的软链接，这样我们就可以很轻松的控制文件名长度了。

不过比较蛋疼的是，我开始的时候写错了，虽然建了软链接，但还是执行的原程序，于是果断怎么都不对，然后为了把长度补回来，我增加了一个argument 2，然后通过这个参数的长度来调节堆栈。

然后就是定位返回地址和buf的间距，仔细看下所给程序main函数的汇编代码，会发现程序在main函数开始：

```
0x804845d <main>:	push   ebp0x804845e <main+1>:	mov    ebp,esp0x8048460 <main+3>:	and    esp,0xfffffff00x8048463 <main+6>:	sub    esp,0x90
```

第三句的`and`由于执行时esp的不同，会导致这个间距发生变化，于是乎，我们还要泄露下ebp，以确定准确的间距（PS：当然，我们也可以重复多次返回地址，因为这个对esp的改动小于16，并且一般是4的倍数吧）。

泄露ebp的话，我们用printf，你用类似格式化字符串溢出漏洞的方式来打印：

```cpp
__asm__("push %ebp");
printf("%1$#x\n");
__asm__("pop %eax");
```

然后我编译运行后发现不对，然后查看编译后的代码，发现：

```
0x804843e <main+33>:	push   ebp0x804843f <main+34>:	mov    DWORD PTR [esp],0x80484f40x8048446 <main+41>:	call   0x80482f0 <printf@plt>0x804844b <main+46>:	pop    eax
```

这里是采用的提前准备好栈的方式，不是临时push的，于是乎，我们要额外push一个空间占位：

```cpp
__asm__("push %ebp");
__asm__("push $0");
printf("%1$#x\n");
__asm__("pop %eax");
__asm__("pop %eax");
```

这样，我们就可以泄露出ebp，从而算出所需padding的长度，然后使程序跳转到shellcode处，拿到shell。