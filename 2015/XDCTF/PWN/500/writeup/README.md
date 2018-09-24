程序在 resit 的时候，对于不合格的 essay，free 和指针的清0是在不同的地方做的，如下：

```c
if ( delete_fail_essay && score <= 59 )
    free(exam->essay);
```

```c
if ( exam->real_essay_len )
{
    exam->essay = 0LL;
    exam->real_essay_len = 0;
}
```

可以明显看到这两个地方的判断条件是不同的，也就是说，我们只要让 `real_essay_len` 为 0，就可以在 essay 被 free 之后仍旧保留此指针，从而实现 UAF。

而在读入 essay 的时候：

```c
read_essay_len = 0;
do
    read_essay_len += read_str(&s[read_essay_len], len - read_essay_len);
while ( read_essay_len != len );
fputs(s, stream);
```

```c
while ( fread(&ptr[i], 1uLL, 1uLL, stream) )
    ++i;
```

很明显，这里我们通过输入 `\x00`，可以导致 `fputs` 的时候没有写入任何东西到 `stream`，于是接下来 `fread` 的时候就什么也读不到，从而实现 `read_essay_len` 为 0。

UAF 之后，我们让 essay 和一个 exam 的结构体使用同一份内存，通过 cheat，我们可以修改已经 free 的 essay，也即可以修改 exam 的结构体，改写其中的函数指针，从而在 show scores 的时候调用任意函数。

但是，调用函数的时候，参数我们无法控制，只能是以执行这个结构体的指针为第一个参数，由于结构体完全受我们控制，也就是说第一个参数的字符串内容是我们可以控制的，那么只要我们能够知道system的地址，我们就可以调用 `system("/bin/sh")` 了。

为了知道 system 的地址，我们可以构造一个格式化字符串漏洞，即调用 `printf("%11$16lx")`，这样可以将 main 函数的 return address 泄漏，而这个地址在 `__libc_start_main` 中，也即在 libc 中，于是就可以计算 system 地址了，此题得以解决。

PS：据说覆盖子进程的 rbp 也是可以脑洞出一个利用的……
