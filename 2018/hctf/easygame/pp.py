#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 hzshang <hzshang15@gmail.com>
#
# Distributed under terms of the MIT license.

from pwn import *
import numpy as np
import scipy.signal as signal

if len(sys.argv) == 1:
    r=remote("127.1",20001)
else:
    r=remote("150.109.119.46",6775)
    r.sendlineafter("hint:","y")
    r.sendlineafter("token:","YCMcAG60fpTxa0MUv5xwLQ6sEIYjS3tJ")

for i in range(8):
    r.recvuntil("[")
    data=r.recvuntil("]")[:-1].split(", ")
    x=np.array(map(float,data))
    sampling_rate = 1500
    fft_size = 1500
    xs = x[:fft_size]
    xf = np.fft.rfft(xs)/fft_size
    freqs = np.linspace(0, sampling_rate/2, fft_size/2+1)
    xfp = 20*np.log10(np.clip(np.abs(xf), 1e-20, 1e100))
    fq = signal.argrelextrema(xfp,np.greater)[0]
    payload = " ".join(map(str,fq))
    print payload
    r.sendline(payload)

r.interactive()



