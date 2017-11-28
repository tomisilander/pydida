#!/usr/bin/python

from bwutil import *
import coliche

def miss_per_row(fn, sep):
    f = file(fn)
    l = f.readline() # Header line
    lineno = 0
    for l in f:
        lineno += 1
        yield (count(re_miss.match, linen2list(l,sep)), lineno)
    f.close()

def main(infile, outfile, sep="\t"):
    of = file(outfile,"w")
    for misscount, lineno in miss_per_row(infile, sep):
        print >>of, misscount, lineno
    of.close()

if __name__ == "__main__":
    coliche.che(main, "infile; outfile; -d --sep sep")
