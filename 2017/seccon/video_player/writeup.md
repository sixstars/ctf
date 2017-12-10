## Vulnerabilities

1. Leak 1 byte in playing VideoClip or AudioClip.

1. When appending subtitle clip, append length could be very large to cause integer overflow in `this->length + append_length`.

## Exploit

Firstly, of course, we need to malloc several times to fill the gaps in heap after random malloc and free operations.

For leaking, seems any bug is ok to leak heap addresss and libc address.

The second bug leads to heap buffer overflow, thus we can overwrite vtable of a clip.
One gadget seems not usable.
So we use the gadget in `setcontext` to call `system("/bin/sh")`.
