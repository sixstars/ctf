#set encoding=utf8

f = open('a.xml','w')

def onedump():
    f.write('<plate>\n')
    f.write('<宫保鸡丁>\n')
    f.write('1\n')
    f.write('</宫保鸡丁>\n')
    f.write('</plate>\n')

def onepush(val):
    f.write('<plate>\n')
    f.write('<paella>\n')
    f.write('%s\n' % val)
    f.write('</paella>\n')
    f.write('</plate>\n')

def oneget():
    f.write('<plate>\n')
    f.write('<불고기>\n')
    f.write('1\n')
    f.write('</불고기>\n')
    f.write('</plate>\n')

def onecheck():
    f.write('<plate>\n')
    f.write('<Борщ>\n')
    f.write('1\n')
    f.write('</Борщ>\n')
    f.write('</plate>\n')

def oneflag():
    f.write('<plate>\n')
    f.write('<दाल>\n')
    f.write('1\n')
    f.write('</दाल>\n')
    f.write('</plate>\n')

def onecmpc():
    f.write('<plate>\n')
    f.write('<ラーメン>\n')
    f.write('1\n')
    f.write('</ラーメン>\n')
    f.write('</plate>\n')

def onecmp():
    f.write('<plate>\n')
    f.write('<stroopwafels>\n')
    f.write('1\n')
    f.write('</stroopwafels>\n')
    f.write('</plate>\n')

def onemov():
    f.write('<plate>\n')
    f.write('<köttbullar>\n')
    f.write('1\n')
    f.write('</köttbullar>\n')
    f.write('</plate>\n')

def onedel():
    f.write('<plate>\n')
    f.write('<γύρος>\n')
    f.write('1\n')
    f.write('</γύρος>\n')
    f.write('</plate>\n')

def oneadd():
    f.write('<plate>\n')
    f.write('<rösti>\n')
    f.write('1\n')
    f.write('</rösti>\n')
    f.write('</plate>\n')

def onesub():
    f.write('<plate>\n')
    f.write('<לאַטקעס>\n')
    f.write('1\n')
    f.write('</לאַטקעס>\n')
    f.write('</plate>\n')

def onemul():
    f.write('<plate>\n')
    f.write('<poutine>\n')
    f.write('1\n')
    f.write('</poutine>\n')
    f.write('</plate>\n')

def onediv():
    f.write('<plate>\n')
    f.write('<ﺢُﻤُّﺻ>\n')
    f.write('1\n')
    f.write('</ﺢُﻤُّﺻ>\n')
    f.write('</plate>\n')

def onejmpif():
    f.write('<plate>\n')
    f.write('<æblegrød>\n')
    f.write('1\n')
    f.write('</æblegrød>\n')
    f.write('</plate>\n')

def value(v):
    return '<value>%s</value>\n' % v

def drink(v):
    f.write('<drinks>%s</drinks>\n' % value(v))

f.write('<meal>\n')

dat = [0]
off = 3
for i in range(32):
    dat.append(2**i)
f.write('<course>\n')
onepush(0)
onepush(32)
onepush(1) # func idx
onepush(1)
onejmpif()
f.write('</course>\n')

# func1: solve once
f.write('<course>\n')
# dec idx
onepush(1)
onepush(1)
onemov()
onesub()
# dup idx
onepush(0)
oneget()
# get 2**i
onepush(off)
oneadd()
oneget()
# dup 2**i
onepush(0)
oneget()
# dup cur
onepush(3)
oneget()

oneadd()
onecmpc()

# negate
onepush(1)
onesub()

onemul()
# add to cur
onepush(2)
oneget()
oneadd()

# delete old cur
onepush(2)
onedel()

# swap cur and idx
onepush(1)
oneget()
onepush(2)
onedel()

onepush(1) # func idx
# dup idx
onepush(1)
oneget()
onedump()

onejmpif()
# drop one
onecheck()
onecheck()

# add outer idx
onepush(1)
oneadd()

onepush(2) # funcidx
# get outer idx
onepush(1)
oneget()
onepush(4)
onecmp()

onejmpif()

onepush(0) # func idx
onepush(1)
onejmpif()


f.write('</course>\n')
# func2 : getflag
f.write('<course>\n')
oneflag()
f.write('</course>\n')


f.write('<state>\n')
for dd in dat:
    drink(dd)
f.write('</state>\n')
f.write('</meal>\n')
