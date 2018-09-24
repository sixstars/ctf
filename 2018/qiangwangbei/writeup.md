# core

/tmp/kallsyms 可以得知 kernel address，过 KASLR

把 offset 改大，`core_read` 可以 leak stack canary

`core_write` 到全局 buf 后，`core_copy_func` 可以 stack overflow，ROP，`commit_creds(prepare_kernel_cred(0))` 提权后，swapgs & iretq get shell

# opm

（感觉不是正解，调试到哭。。。

漏洞是 gets 两次栈溢出，有 stack cookie 不能 ROP，可以覆盖 Role 指针。

由于保护全开，且 gets 末尾一定会产生 `\0`，于是尝试覆盖 Role 低两个 byte，第二个 byte 一定会是 `\0`，于是通过布局，可以控制概率为 1/16 碰撞。

通过一通乱改，将某个 Role 的函数指针从 show 改成 add，通过 list 功能使得可以无限 add，从而拿 shell。
其中需要注意的是中间会有一个 Role 函数指针需要人工控制，而我们最开始没有 leak，故而只能选择使用 vsyscall。

具体见代码，实在太复杂，描述困难。。。


# note

（脑残眼瞎了，当做开了 PIE 做的。。。

修改 title 可以 off by 1，仅可以选择（0x0a 0x21 0x3f 0x40 0x22 0x27 0x23 0x26），其中只有 0x40 可以作为下一个的大小来做 unlink。

首先第一次修改 content 布局，然后修改 title 将 content chunk size 改成 0x40，然后修改 content 利用 realloc 触发 free，此时 content 进了 fastbin 没有 merge 产生 unlink。

然后第三次修改 content 大小为足够大触发 consolidate，使得 unlink 触发，将 title 指向 bss。

通过修改 title 完全控制 bss，进而产生任意读写，最后将 realloc hook 改成 system。
