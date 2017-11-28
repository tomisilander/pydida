#!/usr/bin/python

from bwutil import *
from operator import __add__, __mul__

vdfn, strfn, = n_args_or_bust(2,"vdfile strfile")
valcounts    = map(len, readvdf(vdfn)[1])
parents = cols_n_rest(strfn,2)[2][1:]
parmcs  = [ps==[] and valcounts[i] \
           or valcounts[i]*reduce(__mul__, [valcounts[int(p)] for p in ps]) \
           for i,ps in irange(parents)]

print "\n".join(map(str,parmcs))
print reduce(__add__, parmcs)
