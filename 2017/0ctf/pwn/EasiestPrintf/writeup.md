裸格式化字符串，`printf` 后直接 `_exit`。
修改 `malloc_hook` 为 run shell gadget，然后在 printf payload 后面输出大量字符触发 `malloc`。
