#!/usr/bin/env python
#encoding:utf-8

__all__ = ['SET_PAD_CHAR', 'NOPS', 'LEFT_PAD', 'RIGHT_PAD']

pad_char = '\x90'

def SET_PAD_CHAR(c):
    global pad_char
    pad_char = c

def NOPS(n):
    return pad_char * n

def LEFT_PAD(s, n):
    assert len(s) <= n
    return NOPS(n - len(s)) + s

def RIGHT_PAD(s, n):
    assert len(s) <= n
    return s + NOPS(n - len(s))
