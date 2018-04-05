Vulnerability: off by one.

1. Use off by one to increase size of one fastbin to smallbin, free it, then we can malloc overlapped chunk.

1. With overlap, we can do fastbin attack to write an arbitrary value to main arena.

1. Do fastbin attack again to malloc a fastbin on main arena (treat the value written in last step as chunk size).

1. Modify the the top in main arena, make it point to the address just before `malloc_hook`.

1. Malloc and modify the `malloc_hook`.

1. Enjoy the shell.