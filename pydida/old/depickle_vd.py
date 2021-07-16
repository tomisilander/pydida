#!/usr/bin/env python
from bwutil import *
import pickle

def depickle_vd(fn_in, fn_out):
    f_in  = file(fn_in)
    f_out = file(fn_out,"w")

    try:
        while True: 
            vd = pickle.load(f_in)
            vals = "\t".join(vd['vds'])
            print >>f_out, "%s\t%s" % (vd['name'], vals)
    except EOFError:
        pass
    
if __name__ == "__main__":
    depickle_vd(*(n_args_or_bust("pickled_vd depickled_vd")))
