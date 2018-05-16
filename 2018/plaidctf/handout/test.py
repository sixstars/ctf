def rand_str():
    pool=""
    table="0123456789abcdef"
    for a in table:
        for b in table:
            for c in table:
                for d in table:
                    if a+b+c+d not in pool:
                        pool=pool+a+b+c+d
    return pool

with open("data","w+") as f:
    f.write(rand_str())


