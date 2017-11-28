#!/usr/bin/python

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

def prngs(cmd,bc,vals,divs):
    if bc == 0 : return []
    if cmd == 'NOM' or oneach(vals, divs):
        return map(str, vals)

    pivs = []
    if allints(vals):
        dints = map(int ,map(floor, divs))
        pivs.append(".. %d" % dints[0])
        pivs.extend([x+1<y and "%d .. %d" % (x+1,y) or "%d" % x
                     for x,y in seqzip(dints)])
        pivs.append("%d .." % dints[-1])
    else:
	fmt = "%%.%df" % niceprec(map(float,vals))
        pivs.append("].. %s]" % fmt % divs[0])
        pivs.extend(["]%s .. %s]" %(fmt,fmt) % (x,y)
                     for x,y in seqzip(divs)])
        pivs.append("]%s ..[" %fmt % divs[-1])

    return pivs

def vald(vn, ana, dsp):
    nvals, nfreqs = ana['nvals'] and zip(*ana['nvals']) or ([],[])
    avals, afreqs = ana['avals'] and zip(*ana['avals']) or ([],[])
    return {"name": vn,
            "vds" : prngs(dsp["cmd"], dsp["binc"],
                          nvals, dsp["divs"]) + list(avals)}

def main(anafn, cmdfn, dspfn, vdfile) :
    genmain((anafn,cmdfn,dspfn), (vdfile,), vald, ())

if __name__ == "__main__":
    argscall(main, "anafile cmdfile dspfile vdfile")
