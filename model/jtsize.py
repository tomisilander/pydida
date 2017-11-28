#!/usr/bin/python
from bwutil import *

vdfn, clqfn = n_args_or_bust("vdfile clqfile")

# READ VDFILE TO GET VALUE COUNTS

varnames, valnames = readvdf(vdfn)
varcount,valcounts = len(varnames), map(len,valnames)

# READ CLIQUES AND CALCULATE CLIQUE WEIGHTS 

def clique_pcount(clq) :
    return prod([valcounts[int(i)] for i in clq])

cliques = table_by_rows(clqfn," ")
clique_pcounts = map(clique_pcount,cliques)
tot_pcount = sum(clique_pcounts)

print tot_pcount
