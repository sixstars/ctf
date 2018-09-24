from aes_py import aes128_reverse_keyschedule

res = [
[120, None, None, None, None, None, None, 96, None, None, 3, None, None, 169, None, None],
[None, None, None, 134, None, None, 235, None, None, 191, None, None, 167, None, None, None],
[None, None, 233, None, None, 179, None, None, 155, None, None, None, None, None, None, 157],
[None, 178, None, None, 135, None, None, None, None, None, None, 103, None, None, 151, None],
]

key = [None]*16
for x in res:
    for i, y in enumerate(x):
        if y is not None:
            key[i] = y

print 'Key: '+''.join(map(chr,aes128_reverse_keyschedule(key, 10)))
