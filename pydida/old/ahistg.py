#!/usr/bin/python

def ahistg(vals, tfields):
    fixes = dict([(v,i) for i,v in enumerate(vals)])
    hg = [0]*len(fixes)
    for f in tfields:
        if f in fixes:
            hg[fixes[f]] += 1
    return hg
