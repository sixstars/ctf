#! /bin/sh
#
# gdb.sh
# Copyright (C) 2019 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.
#


gdb \
    -ex 'set arch i386:x86-64:intel' \
    -ex 'target remote localhost:1234' \
#    -ex 'add-symbol-file baby.ko 0xffffffffc0002000' \
    -ex 'continue'

