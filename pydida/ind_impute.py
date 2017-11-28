#!/usr/bin/python

import random

def imputed_line(nline, hst):

    freqs = hst[:]
    mfreq = freqs.pop(-1)

    def impute(n):
        if n== -1:
            try :
                p = random.randrange(sum(freqs))
                s=0
                for i, f in enumerate(freqs):
                    s += f
                    if s > p: return str(i)
            except ValueError: # if all was missing ???
                return str(random.randrage(len(freqs)))
        else:
            return n
        
    return mfreq and map(impute, nline) or nline
