
code = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

table = "OPWvYny#Nopz0$HI34QRSG@dJKq7fghD9Zi*kAB8rsFu56L&Ca^2tTUVEewxlm+/"
new_table = ''
for i in xrange(4):
    s = table[16 * i:][:16]
    tzb = [''] * 16
    for idx, c in enumerate(s):
        tzb[idx ^ i] = c
    new_table += ''.join(tzb)

# code = 'OPWvYny#Nopz0$HI43RQGSd@KJ7qgfDhi*9ZB8kAFursL&562^aCVUTtxweE/+ml'
#print new_table
code = new_table

def encodeBase64(src, encode="utf-8"):

    global code

    paddingTail = {0:'', 8:'0000', 16:'00'}
    paddingEqual = {0:'', 8:'==', 16:'='}

    # src = src.encode(encode)
    sin = ''
    for c in src:
        sin += bin(ord(c))[2:].zfill(8)
    n = len(sin) % 24
    sin += paddingTail[n]

    output = ''
    for i in range(6, len(sin) + 1, 6):
        output += code[int(sin[i - 6:i], 2)]
    output += paddingEqual[n]

    return output


def decodeBase64(src, encode="utf-8"):

    global code
    delPaddingTail = {0:0, 2:4, 1:2}

    value = ''
    n = src.count('=')
    sin = src[:len(src) - n]
    for c in sin:
        value += bin(ord(code.find(c)))[2:].zfill(6)
    value = value[:len(value) - delPaddingTail[n]]

    middle = []
    for i in range(8, len(value) + 1, 8):
        middle.append(int(value[i-8:i], 2))
    output = bytes(middle)#.decode(encoding=encode)

    return output


#print encodeBase64('aaaabaaacaaadaaa')