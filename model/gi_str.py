#!/usr/bin/python

from bwutil import *
from operator import __add__, __mul__

vdfn, strfn, = n_args_or_bust(2,"vdfile strfile")
varcount= rowc(vdfn)

strf = open(strfn,"w")
print >>strf, varcount
for i in xrange(varcount): print >>strf, "0 0"
strf.close()
