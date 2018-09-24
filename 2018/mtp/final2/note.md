```python

d = {}
d[26] = 8
d[2] = 6
d[35] = d[55] = d[57] = d[61] = 36
d[31] = 11
d[51] = 26
d[46] = 44
d[13] = 7
d[18] = 4
d[4] = 38
d[39] = 37
d[34] = d[40] = d[41] = d[60] = 1
d[5] = d[9] = d[10] = d[37] = 30
d[53] = 33
d[42] = 35
d[56] = 34
d[59] = 3
d[12] = 43
d[6] = d[7] = d[22] = d[27] = 0
d[11] = d[16] = 47
d[31] = 11
d[32] = 29
d[14] = 7
d[52] = 28
d[48] = 31
d[38] = 32
d[44] = 39
d[50] = 40
d[21] = 16
d[36] = 19
d[47] = 14
d[49] = 13
d[30] = 15
d[29] = 10
d[8] = d[23] = d[17] = d[54] = 5
d[33] = 41
d[3] = 42
d[20] = 45
print len(d.keys()), len(set(d.keys()))
print len(d.values()), len(set(d.values()))

tzb = [i for i in xrange(64)]
for k, v in d.iteritems():
    tzb[k] = v
print json.dumps(tzb)

```