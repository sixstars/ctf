
n2ch = "".join([
    "abcdefghijklmnopqrstuvwxyz",
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "0123456789+/",
])
ch2n = dict(zip(n2ch, range(len(n2ch))))

def separate(seq, size):
    return (seq[i:i+size] for i in range(0, len(seq), size))

def encode(data, split=76, br="\r\n"):
    """ base64 encoder:
    - data: data bytes
    - split: size of each lines
    - br: line break
    """
    buf = ""
    rem = len(data) % 3
    pad = 3 - rem
    if rem > 0: data = data + "\0" * pad
    for i in range(0, len(data), 3):
        b3 = (ord(data[i]) << 16) | (ord(data[i + 1]) << 8) | ord(data[i + 2])
        buf += n2ch[b3 >> 18] + n2ch[(b3 >> 12) & 0x3f]
        buf += n2ch[(b3 >> 6) & 0x3f] + n2ch[b3 & 0x3f]
        pass
    if rem > 0: buf = buf[:-pad] + "=" * pad
    return br.join(separate(buf, split)) + br if split > 0 else buf

def decode(base64):
    """base64 decoder:
    - base64: base64 string
    """
    ns = []
    for ch in base64:
        if ch == "=": break
        try: ns.append(ch2n[ch])
        except: pass
        pass
    data = ""
    rem = len(ns) % 4
    # Invalid when rem is 3. But run as if the last chunk does not exist
    if rem > 0: ns += [0] * (4 - rem)
    for i in range(0, len(ns), 4):
        b3 = (ns[i] << 18) | (ns[i + 1] << 12) | (ns[i + 2] << 6) | ns[i + 3]
        data += chr(b3 >> 16) + chr((b3 >> 8) & 0xff) + chr(b3 & 0xff)
        pass
    return data[:-rem] if rem > 0 else data
