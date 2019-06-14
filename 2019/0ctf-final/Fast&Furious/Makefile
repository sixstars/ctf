#
# Makefile
# hzshang, 2019-06-08 14:54
#

all:
	@echo "Makefile needs your attention"
	gcc main.c -o main -static
	strip main
	cp main initramfs/home/pwn/
	cd initramfs && find . | cpio -o --format=newc > ../initramfs.cpio


