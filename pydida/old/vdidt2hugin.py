#!/usr/bin/python

from bwutil import *
import coliche

def main(vdfile, idtfile):
    varnames, valcounts  = readvdf(vdfile)
    data = table_by_rows(idtfile)

    print ",".join(varnames)
    for r in data:
        print ",".join(r)

if __name__ == "__main__":
    coliche.che(main, "vdfile; idtfile")
