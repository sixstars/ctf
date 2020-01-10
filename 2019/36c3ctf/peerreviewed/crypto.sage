#!/usr/bin/env sage

# A. G. D. Uchoa, M. E. Pellenz, A. O. Santin, and C. A. Maziero.
# "A three-pass protocol for cryptography based on padding for wireless networks."
# In: 2007 4th IEEE Consumer Communications and Networking Conference.
# IEEE, Jan. 2007, pp. 287--291. DOI: 10.1109/CCNC.2007.63.
#
# For those without IEEE subscriptions, this paper is also available through
# ResearchGate and Google Scholar.

from itertools import izip_longest

import struct

def long_to_bytes(n, blocksize=0):
    """long_to_bytes(n:long, blocksize:int) : string
    Convert a long integer to a byte string.

    If optional blocksize is given and greater than zero, pad the front of the
    byte string with binary zeros so that the length is a multiple of
    blocksize.
    """
    # after much testing, this algorithm was deemed to be the fastest
    s = ''
    n = long(n)
    pack = struct.pack
    while n > 0: 
        s = pack('>I', n & 0xffffffffL) + s
        n = n >> 32
    # strip off leading zeros
    for i in range(len(s)):
        if s[i] != '\000'[0]:
            break
    else:
        # only happens when n == 0
        s = '\000'
        i = 0
    s = s[i:]
    # add back some pad bytes.  this could be done more efficiently w.r.t. the
    # de-padding being done above, but sigh...
    if blocksize > 0 and len(s) % blocksize:
        s = (blocksize - len(s) % blocksize) * '\000' + s
    return s

def bytes_to_long(s):
    """bytes_to_long(string) : long
    Convert a byte string to a long integer.

    This is (essentially) the inverse of long_to_bytes().
    """
    acc = 0L 
    unpack = struct.unpack
    length = len(s)
    if length % 4: 
        extra = (4 - length % 4) 
        s = '\000' * extra + s
        length = length + extra
    for i in range(0, length, 4):
        acc = (acc << 32) + unpack('>I', s[i:i+4])[0]
    return acc


# Settings from Section IV of the paper
R = RealField(prec=200)
block_size = 192

# Key generation
def rotate_2d(field, theta):
    # Rotation matrix (clockwise, as in Section III)
    return matrix(field, [[cos(theta), sin(theta)], [-sin(theta), cos(theta)]])

def generate_key():
    # Pick a random angle on the unit circle
    circle = 2 * R.pi()
    theta = R(random()) * circle
    # Follow Section III to generate the rest of the key:
    # Build the rotation matrix O and its inverse
    O = rotate_2d(R, theta)
    Oc = rotate_2d(R, circle - theta)
    # Generate the nonce matrix (with 1 <= a, b <= 2**64)
    a = randint(1, 2**64)
    b = randint(1, 2**64)
    A = matrix(R, [[a, b], [-b, a]])
    Ac = A.transpose() / A.det()
    return O, Oc, A, Ac

# Message handling
def split_message(message, block_size):
    # Convert to bits
    message = Integer(bytes_to_long(message)).bits()
    # Add padding
    message += [1]
    padding_required = block_size - len(message) % block_size
    if padding_required != block_size:
        message += [0] * padding_required
    # Split into blocks
    for block_start in range(0, len(message), block_size):
        yield Integer(message[block_start:block_start+block_size][::-1], base=2)

def merge_message(blocks):
    # Merge blocks
    print blocks[0]
    blocks = [Integer(round(block)).bits()[::-1] for block in blocks]
    blocks = [[0] * (block_size - len(block)) + block for block in blocks]
    bits = flatten(blocks)
    # Remove padding
    bits = bits[:-bits[::-1].index(1)-1]
    # Convert back
    return long_to_bytes(Integer(bits, base=2))

def group(iterable, n, fill=None):
    iters = [iter(iterable)] * n
    return izip_longest(*iters, fillvalue=fill)


def recover(a,b):
    x0 = (a[0]*b[0]+a[1]*b[1])/(a[0]^2+a[1]^2)
    x1 = (a[0]*b[1]-a[1]*b[0])/(a[0]^2+a[1]^2)
    return vector(R, [x0, x1])

def getx(a,b,c):
    x0,x1 = recover(b,a)
    t0=c[0]*x0-c[1]*x1
    t1=c[0]*x1+c[1]*x0
    return vector(R, [t0, t1])

# Self-test for encryption and decryption
if __name__ == '__main__':
    a1,b1,c1,a2,b2,c2,a3,b3,c3 = [(5.8537179772742871378006829317359804640034149162093776176771e75, 2.0260990893806965307943860314007373888732002921518840941414e76)
, (4.0652782673020986683538918237010543408982543019306057179496e95, -5.0285426513783822097670201376390415563936061484095492229894e94)
, (4.3083595977562861674637990303350994431503203162436044206961e76, -3.1928247205608247346546681530367209122491766171698701927922e76)
, (3.9886651421460868244883042163468164077791762065632163641999e76, -1.2487387183806776412156661578750877275468860853692530589115e77)
, (2.5644531171906756537679808003501733255703504126650573479133e95, -1.6570541229598112699074962433815055733294177769576178678896e96)
, (4.5893614625576224795913782492661186902913334535507951850089e76, 6.8611881934867127810471276550294069221078140676008042683634e76)
, (-6.5089227887140404010136240391818701730482514213358150433451e75, 5.5620733870042242270647223203879530885369669489378834804472e76)
, (1.0017374772520318947002755790705886607122203555146923369286e95, 1.2876407911288161811207561236370324382394428286338064237471e96)
, (1.1418280384822587553925695577555385627605037374102719431688e77, -1.9966984339634055590175475802847306340483261373340080568330e76)]
    results = []
    results.extend(getx(a1,b1,c1))
    results.extend(getx(a2,b2,c2))
    results.extend(getx(a3,b3,c3))
    print parent(results[0])
    print results
    m = merge_message(results)
    print m
    exit()
    #from message import m
    m = 't'*49
    blocks = split_message(m, block_size)
    results = []
    for b1, b2 in group(blocks, 2, Integer(0)):
        b = vector(R, [b1, b2])
        # Generate keys for both sides
        O1, Oc1, A1, Ac1 = generate_key()
        O2, Oc2, A2, Ac2 = generate_key()
        # Simulate transmission
        yA = b * O1 * A1
        print 'A -> B: yA =', yA
        yB = yA * O2 * A2
        print 'B -> A: yB =', yB
        yC = yB * Oc1 * Ac1
        print 'A -> B: yC =', yC
        x = yC * Oc2 * Ac2
        # Collect results
        results.extend(x)
    print results
    assert m == merge_message(results), 'Test failed'
