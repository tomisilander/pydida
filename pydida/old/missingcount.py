#!/usr/bin/env python
from bwutil import *
import coliche

def main(filename):

    df = file(filename)
    df.readline() # Read headerline

    n=0
    for l in df:
        n+=1
        print "%d\t%d" % (n,count(re_miss.match, l[:-1].split("\t")))

        df.close()

coliche.che(main, "filename")
