#!/usr/bin/env python
from bwutil import *
import coliche

def main(vdfile, idtfile):
    varnames, valcounts  = readvdf(vdfile)
    data = table_by_rows(idtfile)
    
    classix = varnames.index("class")

    print ",".join(varnames[0:classix]+varnames[classix+1:])
    for r in data: print ",".join(r[0:classix]+r[classix+1:])

coliche.che(main, "vdfile; idtfile;")

