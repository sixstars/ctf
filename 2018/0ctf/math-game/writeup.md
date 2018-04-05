Reverse the binary, we know that once we can calculate the difference for two random integer with `printf`, we can get the flag.

In order to do calculation, we need to know some tips about `printf`.

1. `%5$x` will use the 5th format parameter for `%x`.

1. `%n` is widely used for `printf` vulnerability, it will write the number of characters that have been output by `printf` to given address.

1. `%*5$c` will pad the result of `%c`, make the length of output equals the value of 5th format parameter.

Now, we can make some atomic operation.

1. `%{}c%9$n`: Write constant to arbitrary address, can be expanded to word/byte writing.

1. `%*5$c%9$n`: Move integer to arbitrary address, can be expanded to word/byte moving.

1. `%*5c%*6c%9$n`: Add two integer, can be expanded to word/byte adding.

1. `%*5$c%*5$c%9$n`: Left shift one. With left shift one and misplaced reading and writing, we can extract the most significant bit of one byte.

1. Flip bit: `byte(1 + 255) == 0`, `byte(0 + 255) == 1`

As we know, in current computer, we have `x - y == x + (-y) == x + (~y + 1)`, so we can flip all bit of `y` to get the result of subtraction.

Things will go worse in detail:

1. `%*5$c` will output one char no matter the 5th parameter is 0x0 or 0x1. So we need to distinguish 0x0 and 0x1 by distinguishing 0x0 and 0x100.

1. `%*5$c` will output 11 chars if the 5th parameter is -11. In the binary, the random value is guaranteed to be positive (except 0), which means that the opposite value will always be negative.

In fact, with the help of above detail, we can flip all bits of one positive integer by flip its significant bit from 0 to 1. It could make things easier.
