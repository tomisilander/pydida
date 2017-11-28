#!/usr/bin/python
from bwutil import *
import math 

sstfn, = n_args_or_bust("sstfn")
sst   = table_by_rows(sstfn," ")

def frqTerm(f,n):
    if f==0.0 : return 0.0
    else    : return f * math.log(f/n)

def frqsLogMl(lst):
    flst = map(float,lst)
    n    = sum(flst)
    if n == 0.0 : return 0.0
    else :        return sum([frqTerm(f,n) for f in flst])
    
def varLogMl(pcc,sst):
    varss = sst[:pcc]
    sst[:pcc] = []
    return sum(map(frqsLogMl, varss))
    
totLogMl = 0.0
while sst != []:
    pcc = int(sst.pop(0)[0])
    totLogMl += varLogMl(pcc,sst)

print totLogMl
