#!/bin/bash

stty intr ^]
cd `dirname $0`
if [ -z $1 ]
then
    debug=""
else
    debug="-s -S"
fi
sudo qemu-system-x86_64 \
    -m 256M \
    -nographic \
    -enable-kvm \
    -kernel bzImage \
    -append 'console=ttyS0 loglevel=3 oops=panic panic=1 nokaslr' \
    -monitor /dev/null \
    -initrd initramfs.cpio \
    -smp cores=1,threads=1 \
    -cpu qemu64,smep $debug #2>/dev/null


