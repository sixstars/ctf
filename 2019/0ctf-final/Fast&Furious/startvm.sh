#!/bin/bash

stty intr ^]
cd `dirname $0`
qemu-system-x86_64 \
    -m 256M \
    -nographic \
    -kernel bzImage \
    -append 'console=ttyS0 loglevel=3 oops=panic panic=1 kaslr' \
    -monitor /dev/null \
    -initrd initramfs.cpio \
    -smp cores=4,threads=4 \
    -cpu kvm64
    #-enable-kvm \
