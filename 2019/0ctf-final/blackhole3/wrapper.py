#!/usr/bin/python3 -u
# encoding: utf-8
import random, string, subprocess, os, sys, tempfile, time
from hashlib import sha256
root = os.path.dirname(os.path.realpath(__file__))
os.chdir(os.path.dirname(os.path.realpath(__file__)))

def proof_of_work():
    chal = ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(16))
    print(chal)
    chal = chal.encode("latin-1")

    sol = sys.stdin.readline().strip()
    sol_bytes = bytes.fromhex(sol)
    if not sha256(chal + sol_bytes).hexdigest().startswith('000000'): # please, do not bruteforce any thing
        sys.exit()

def exec_serv(name, payload):
    suffix = '_' + ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(16))
    secret = ''.join(random.choice(string.ascii_letters+string.digits) for _ in range(1024))
    secret = secret.encode("latin-1")
    prefix = 'blackhole_'
    with tempfile.TemporaryDirectory(suffix, prefix) as cwd:
        with open(os.path.join(cwd, "secret"), "wb") as f:
            f.write(secret)
        previous_t = time.time()
        p = subprocess.Popen([name], bufsize=0, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,cwd=cwd)
        count = p.stdin.write(payload)
        assert count == len(payload)
        p.wait()

        if time.time() - previous_t > 5:
            print("too slow")
            return False
        output = p.stdout.read(1024)
        p.stdin.close()
        p.stdout.close()
        return output == secret
    return False

if __name__ == '__main__':
    #proof_of_work()
    print("show me the rop chain(in hex):")
    payload = sys.stdin.readline().strip()
    payload_bytes = bytes.fromhex(payload)
    print(len(payload_bytes))
    for i in range(3000): # your exploit must be stable
        if not i%50:
            print(i)
        try:
            if not exec_serv(os.path.join(root, './blackhole3'), payload_bytes):
                print("fail")
                sys.exit(-1)
        except Exception as e:
            print(e)
            print("error")
            sys.exit(-1)
    with open("/flag", "rb") as f:
        print(f.read())


