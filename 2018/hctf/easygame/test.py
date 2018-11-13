# -*- coding: utf-8 -*-
import numpy as np
import pylab as pl

sampling_rate = 1500
fft_size = 1500
t = np.arange(0, 1.0, 1.0/sampling_rate)
with open("log","r") as f:
	x=map(float,f.read().split("\n")[:-1])


xs = x[:fft_size]
xf = np.fft.rfft(xs)/fft_size
freqs = np.linspace(0, sampling_rate/2, fft_size/2+1)
xfp = 20*np.log10(np.clip(np.abs(xf), 1e-20, 1e100))
pl.figure(figsize=(8,4))
pl.subplot(211)
pl.plot(t[:fft_size], xs)
pl.xlabel(u"时间(秒)")
pl.title(u"156.25Hz和234.375Hz的波形和频谱")
pl.subplot(212)
pl.plot(freqs, xfp)
pl.xlabel(u"频率(Hz)")
pl.subplots_adjust(hspace=0.4)
pl.show()