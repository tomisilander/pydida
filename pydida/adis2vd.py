#!/usr/bin/env python
from math import ceil, floor, log10
from dispoint import seqzip

from itertools import starmap

def niceprec(vals) :
    mind = min(starmap, seqzip(vals))
    return mind>=1 and 1 or mind>0 and ceil(-log10(mind)) or 4

def oneach(vals, divs) :
    if len(vals)-len(divs) == 1:
        vds = list(sum(zip(vals,divs),(vals[-1],)))
        vds_sorted = vds[:]; vds_sorted.sort()
        return vds == vds_sorted
    else:
        return False

def allints(vals): 
    for v in vals:
        if not isinstance(v, int): return False
    return True

def int_range(x,y):
    if (x+1>=y):
        return "%d" % x
    else:
        return "[%d .. %d]" % (x,y)

def prngs(cmd,bc,vals,divs, use_limits):
    if bc == 0 : return []
    if cmd == 'NOM' or oneach(vals, divs):
        return map(str, vals)

    pivs = []
    min_val, max_val = vals[0], vals[-1]
    if allints(vals):
        dints = map(int ,map(floor, divs))
        if use_limits:
            pivs.append(int_range(min_val, dints[0]))
            pivs.extend([int_range(x+1,y) for x,y in seqzip(dints)])
            pivs.append(int_range(dints[-1]+1, max_val))
        else:
            pivs.append(".. %d" % dints[0])
            pivs.extend([x+1<y and "%d .. %d" % (x+1,y) or "%d" % x
                         for x,y in seqzip(dints)])
            pivs.append("%d .." % dints[-1])
    else:
    	fmt = "%%.%df" % niceprec(map(float,vals))
        if use_limits:
            pivs.append("[%s .. %s]" % (fmt,fmt) % (min_val, divs[0]))
            pivs.extend(["]%s .. %s]" %(fmt,fmt) % (x,y)
                        for x,y in seqzip(divs)])
            pivs.append("]%s .. %s]" % (fmt,fmt) % (divs[-1], vals[-1]))
        else:
            pivs.append("].. %s]" % fmt % divs[0])
            pivs.extend(["]%s .. %s]" %(fmt,fmt) % (x,y)
                        for x,y in seqzip(divs)])
            pivs.append("]%s ..[" % fmt % divs[-1])

    return pivs

def vald(vn, ana, dsp, use_limits):
    nvals, nfreqs = ana['nvals'] and zip(*ana['nvals']) or ([],[])
    avals, afreqs = ana['avals'] and zip(*ana['avals']) or ([],[])
    return {"name": vn,
            "vds" : prngs(dsp["cmd"], dsp["binc"], nvals, dsp["divs"], 
                    use_limits) + list(avals)}

def main(anafn, cmdfn, dspfn, vdfile) :
    genmain((anafn,cmdfn,dspfn), (vdfile,), vald, ())

if __name__ == "__main__":
    argscall(main, "anafile cmdfile dspfile vdfile")
