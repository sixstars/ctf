#!/usr/bin/env python
#encoding:utf-8

def NOPS(n):
    return '\x90' * n

def LEFT_PAD(s, n):
    assert len(s) <= n
    return NOPS(n - len(s)) + s

def RIGHT_PAD(s, n):
    assert len(s) <= n
    return s + NOPS(n - len(s))
