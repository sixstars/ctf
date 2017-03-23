#!/bin/bash
rm cpio/exp
musl-gcc -Os -static exploit.c -lutil -o cpio/exp
cd cpio
find . | cpio -H newc -o > ../rootfs.cpio
