import sys
import os
import random
import time
import base64
import string
import hashlib
from pwn import *
# os.chdir("/home/ctf")
env = {"LD_PRELOAD": os.path.join(os.getcwd(), "scf.so")}
SALT_LEN = 10
HEX_LEN = 4


def base_str():
    return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def random_string(length):
    string = [random.choice(base_str()) for i in range(length)]
    return ("".join(string))


def tofile(data):
    try:
        data = base64.b64decode(data)
    except:
        return ""
    cur_time = str(time.time())
    filename = "./backup/" + cur_time + ".elf"
    fd = open(filename, "wb")
    fd.write(data)
    fd.close()
    filename = "./" + cur_time + ".elf"
    fd = open(filename, "wb")
    fd.write(data)
    fd.close()
    return filename


def main():
    """
    salt = random_string(SALT_LEN)
    tmpvalue = random_string(20) + salt
    md5 = hashlib.md5()
    md5.update(tmpvalue.encode("utf-8"))
    submd5 = md5.hexdigest()[:4]
    print("[*]Proof of work:")
    print("\tMD5(key+\"%s\")[:4]==%s" % (salt, submd5))
    print("[+]Give me the key:")
    sys.stdout.flush()
    value = sys.stdin.readline()[:-1]
    value = value + salt
    md5 = hashlib.md5()
    md5.update(value.encode("utf-8"))
    md5value = md5.hexdigest()
    if (md5value[:HEX_LEN] != submd5):
        print("[-]Access Failed")
        return
    """
    print("[+]escape the sandbox!")
    sys.stdout.flush()
    ELF = sys.stdin.readline()[:-1]
    print(len(ELF))
    if (len(ELF) > 1048576):
        print("[-]ELF too big!")
        return
    elfname = tofile(ELF)
    if elfname == "":
        print("[-]base64 please!")
        sys.stdout.flush()
        return
    os.system("chmod +x %s" % elfname)
    io = process(elfname, env=env)
    io.interactive()


main()
