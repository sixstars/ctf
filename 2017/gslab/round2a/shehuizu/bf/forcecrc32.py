#
# CRC-32 forcer (Python)
# Compatible with Python 2 and 3.
#
# Copyright (c) 2017 Project Nayuki
# https://www.nayuki.io/page/forcing-a-files-crc-to-any-value
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (see COPYING.txt).
# If not, see <http://www.gnu.org/licenses/>.
#

import os, sys, zlib


# ---- Main application ----

def main(args):
    # Handle arguments
    if len(args) != 3:
        return "Usage: python forcecrc32.py FileName ByteOffset NewCrc32Value"
    try:
        offset = int(args[1])
    except ValueError:
        return "Error: Invalid byte offset"
    if offset < 0:
        return "Error: Negative byte offset"
    try:
        if len(args[2]) != 8 or args[2].startswith(("+", "-")):
            return "Error: Invalid new CRC-32 value"
        temp = int(args[2], 16)
        if temp & MASK != temp:
            return "Error: Invalid new CRC-32 value"
        new_crc = reverse32(temp)
    except ValueError:
        return "Error: Invalid new CRC-32 value"

    # Process the file
    try:
        modify_file_crc32(args[0], offset, new_crc, True)
    except IOError as e:
        return "I/O error: " + str(e)
    except ValueError as e:
        return "Error: " + str(e)
    except AssertionError as e:
        return "Assertion error: " + str(e)
    return None


from StringIO import StringIO
def crack_crc32(s, newcrc, init_crc=None, printstatus=False):
    raf = StringIO(s + '\x00' * 4)
    newcrc = int(bin(newcrc)[2:].rjust(32, '0')[::-1], 2)
    raf.seek(0, os.SEEK_END)
    length = raf.tell()
    offset = length - 4
    if offset + 4 > length:
        raise ValueError("Byte offset plus 4 exceeds file length")

    # Read entire file and calculate original CRC-32 value
    crc = get_crc32(raf, init_crc)
    if printstatus:
        print("Original CRC-32: {:08X}".format(reverse32(crc)))

    # Compute the change to make
    delta = crc ^ newcrc
    delta = multiply_mod(reciprocal_mod(pow_mod(2, (length - offset) * 8)), delta)

    # Patch 4 bytes in the file
    raf.seek(offset)
    bytes4 = bytearray(raf.read(4))
    if len(bytes4) != 4:
        raise IOError("Cannot read 4 bytes at offset")
    for i in range(4):
        bytes4[i] ^= (reverse32(delta) >> (i * 8)) & 0xFF
    return bytes4


# ---- Main function ----

# Public library function. path is str/unicode, offset is uint, newcrc is uint32, printstatus is bool.
# Returns None. May raise IOError, ValueError, AssertionError.
def modify_file_crc32(path, offset, newcrc, printstatus=False):
    with open(path, "r+b") as raf:
        raf.seek(0, os.SEEK_END)
        length = raf.tell()
        if offset + 4 > length:
            raise ValueError("Byte offset plus 4 exceeds file length")

        # Read entire file and calculate original CRC-32 value
        crc = get_crc32(raf)
        if printstatus:
            print("Original CRC-32: {:08X}".format(reverse32(crc)))

        # Compute the change to make
        delta = crc ^ newcrc
        delta = multiply_mod(reciprocal_mod(pow_mod(2, (length - offset) * 8)), delta)

        # Patch 4 bytes in the file
        raf.seek(offset)
        bytes4 = bytearray(raf.read(4))
        if len(bytes4) != 4:
            raise IOError("Cannot read 4 bytes at offset")
        for i in range(4):
            bytes4[i] ^= (reverse32(delta) >> (i * 8)) & 0xFF
        raf.seek(offset)
        raf.write(bytes4)
        if printstatus:
            print("Computed and wrote patch")

        # Recheck entire file
        if get_crc32(raf) != newcrc:
            raise AssertionError("Failed to update CRC-32 to desired value")
        elif printstatus:
            print("New CRC-32 successfully verified")


# ---- Utilities ----

POLYNOMIAL = 0x104C11DB7  # Generator polynomial. Do not modify, because there are many dependencies
MASK = (1 << 32) - 1


def get_crc32(raf, start=None):
    raf.seek(0)
    crc = 0
    while True:
        buffer = raf.read(128 * 1024)
        if len(buffer) == 0:
            return reverse32(crc & MASK)
        else:
            crc = zlib.crc32(buffer, start)


def reverse32(x):
    y = 0
    for i in range(32):
        y = (y << 1) | (x & 1)
        x >>= 1
    return y


# ---- Polynomial arithmetic ----

# Returns polynomial x multiplied by polynomial y modulo the generator polynomial.
def multiply_mod(x, y):
    # Russian peasant multiplication algorithm
    z = 0
    while y != 0:
        z ^= x * (y & 1)
        y >>= 1
        x <<= 1
        if (x >> 32) & 1 != 0:
            x ^= POLYNOMIAL
    return z


# Returns polynomial x to the power of natural number y modulo the generator polynomial.
def pow_mod(x, y):
    # Exponentiation by squaring
    z = 1
    while y != 0:
        if y & 1 != 0:
            z = multiply_mod(z, x)
        x = multiply_mod(x, x)
        y >>= 1
    return z


# Computes polynomial x divided by polynomial y, returning the quotient and remainder.
def divide_and_remainder(x, y):
    if y == 0:
        raise ValueError("Division by zero")
    if x == 0:
        return (0, 0)

    ydeg = get_degree(y)
    z = 0
    for i in range(get_degree(x) - ydeg, -1, -1):
        if (x >> (i + ydeg)) & 1 != 0:
            x ^= y << i
            z |= 1 << i
    return (z, x)


# Returns the reciprocal of polynomial x with respect to the modulus polynomial m.
def reciprocal_mod(x):
    # Based on a simplification of the extended Euclidean algorithm
    y = x
    x = POLYNOMIAL
    a = 0
    b = 1
    while y != 0:
        q, r = divide_and_remainder(x, y)
        c = a ^ multiply_mod(q, b)
        x = y
        y = r
        a = b
        b = c
    if x == 1:
        return a
    else:
        raise ValueError("Reciprocal does not exist")


def get_degree(x):
    return x.bit_length() - 1


# ---- Miscellaneous ----

if __name__ == "__main__":
    errmsg = main(sys.argv[1:])
    if errmsg is not None:
        sys.exit(errmsg)
