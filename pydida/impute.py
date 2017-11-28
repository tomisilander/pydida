import random

def impute_GI(nfields, freqs, seed = None):
    if seed: random.seed(seed)
    choices = map(str, range(len(freqs)-1))
    return map(int, ((n==-1 and random.choice(choices) or n) for n in nfields))

def impute(nfields, freqs, impcmd):
    if impcmd[0] == 'GI':
        return impute_GI(nfields, freqs, *impcmd[1:])
    else: # INCLUDING NONE
        return nfields
