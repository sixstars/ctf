import sys

# see README for details

def encode(cmd):
    def conv(c):
        """ Converts a character to its octal representationn """
        m = { '0' : '$#',
                '1' : '${##}',
                '2' : '$((${##}<<${##}))',
                '3' : '$(($((${##}<<${##}))#${##}${##}))',
                '4' : '$((${##}<<${##}<<${##}))',
                '5' : '$(($((${##}<<${##}<<${##}))#${##}${##}))',
                '6' : '$(($((${##}<<${##}))#${##}${##}$#))',
                '7' : '$(($((${##}<<${##}))#${##}${##}${##}))',
                '8' : '$((${##}<<${##}<<${##}<<${##}))'
        }
        n = map(lambda x: m[x], list(str(oct(ord(c)))[2:]))
        return "\\\\" + ''.join(n)

    res = "{"
    for c in cmd.split(): 
        res += "$\\'"
        res += ''.join(map(conv, list(c)))
        res += "\\',"

    res += "}"

    return res


def encode_file(file):
    lines = open(file).read().split("\n")
    payload = ""
    for line in lines:
        if line.strip() == "" or line.strip().startswith("#"):
            continue
        payload += line + " "
        if not line.strip().endswith("&"): 
            payload += "; "
    return encode_cmds("eval " + payload)


def encode_cmds(cmd):
    sys.stderr.write(cmd + "\n")
    res = "${!#}<<<" +encode(cmd)
    return res


if sys.argv[1] == "file":
    print(encode_file(sys.argv[2]))
else:
    print(encode_cmds(sys.argv[1]))
