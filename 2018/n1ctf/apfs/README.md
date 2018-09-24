```bash
cat time2.txt | awk '{print $2}' | awk -F. '{printf "%s00000000\n", $2}' | python -c "for i in xrange(531): print raw_input()[6:][:3]" > tmp2
```

```python
382/1: from pwn import *
382/2: f1 = read('tmp1')
382/3: f2 = read('tmp2')
382/4: f1
382/5: f2
382/6: map(int,f1.split('\n'))
382/7: f1.split('\n')
382/8: [int(i, 10) for i in f1.split('\n')]
382/9: [int(i, 10) for i in f1.split('\n')[:-1]]
382/10: a1 = [int(i, 10) for i in f1.split('\n')[:-1]]
382/11: a2 = [int(i, 10) for i in f2.split('\n')[:-1]]
382/12: a1
382/13: a2
382/14: xor(a1, a2)
382/15: 531*3
382/16: 531*3/8
382/17: 199*8
382/18: [bin(x) for x in xor(a1, a2)]
382/19: [bin(ord(x)) for x in xor(a1, a2)]
382/20: ['%03b' %(ord(x)) for x in xor(a1, a2)]
382/21: [bin(ord(x)) for x in xor(a1, a2)]
382/22: [bin(ord(x))[2:] for x in xor(a1, a2)]
382/23: [bin(ord(x))[2:].rjust(3) for x in xor(a1, a2)]
382/24: [bin(ord(x))[2:].rjust(3, '0') for x in xor(a1, a2)]
382/25: ''.join([bin(ord(x))[2:].rjust(3, '0') for x in xor(a1, a2)])
382/26: unbits(''.join([bin(ord(x))[2:].rjust(3, '0') for x in xor(a1, a2)]))
382/27: write('x.zip', unbits(''.join([bin(ord(x))[2:].rjust(3, '0') for x in xor(a1, a2)])))
382/28: len(''.join([bin(ord(x))[2:].rjust(3, '0') for x in xor(a1, a2)]))
382/29: 15bc
382/30: len(unbits(''.join([bin(ord(x))[2:].rjust(3, '0') for x in xor(a1, a2)])))
382/31: 200*8
382/32: write('x.zip', unbits(''.join([bin(ord(x))[2:].rjust(3, '0') for x in xor(a1, a2)]))[:-1])

```
