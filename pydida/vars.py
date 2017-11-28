def vars(vnfile):
    return filter(None, map(str.strip, file(vnfile)))

def var(vnfile, vix):
    return vars(vnfile)[vix]
