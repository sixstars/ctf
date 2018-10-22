qemu-system-x86_64 -monitor /dev/null -m 64 -nographic -kernel "bzImage" -initrd initrd.cpio -append "console=ttyS0 init='/init'"
