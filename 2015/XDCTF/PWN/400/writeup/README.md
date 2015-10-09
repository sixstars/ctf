逆向可发现如下一段：

```c
if ( (unsigned __int16)(file_name_len + 2) <= (signed int)(buf - src + buf_len - 46) )
{
    if ( file_name_len )
        s = read_str(&ptr_int16, file_name_len, 1);
    v3 = strlen(s);
    v11 = write(fd, s, v3);
}
```

很明显，这里如果`file_name_len`是0xffff的话导致加法溢出的话，这里的判断过掉，而后面又会将其当成一个无符号数去读字符串，从而输出后面的内存，其中就包含了flag。
