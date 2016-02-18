和 note2 一样无限读入，随便越界，unlink 将 note 指向 got 表后，由于没有 show 不能泄漏，于是先改 free 为 puts，用 delete note 来泄漏，然后改 atoi 为 system 即可。

PS：这完全就是 note2 exp 稍微加点料，越加分越低算 what gui :flushed:
