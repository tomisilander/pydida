#!/usr/bin/python

from bwutil import *
from operator import __add__, __mul__

vdfn, classixs, strfn, = n_args_or_bust(3,"vdfile classix strfile")
classix = int (classixs)
varcount= rowc(vdfn)

strf = open(strfn,"w")
print >>strf, varcount
for i in xrange(varcount): 
	if i==classix : print >>strf, "%d 0" % (varcount-1)
	else: print >>strf, "0 1 %d" % classix
strf.close()
