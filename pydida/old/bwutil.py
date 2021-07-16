#!/usr/bin/env python
import sys, os, operator
import re
from types import *
from itertools import chain,izip,repeat
import itertools

bwbindir=os.environ.get("%s/bin"%"BAYWAYHOME",
                        "%s/bw/bin" % os.environ['HOME'])

re_miss = re.compile("^\s*$")
re_num  = re.compile("^\s*-?(?:\d+\.?\d*|\.\d+)\s*$")
re_int = re.compile("^\s*-?\d+\s*$")

def typefy1(s):
    if   re_int.match(s): return int(s)
    elif re_num.match(s): return float(s)
    else                : return s
    
def typefy(ss): map(typefy1,ss)

def fst(x): return x[0]
def snd(x): return x[1]
def eq1(x): return lambda y: y==x
def ident(x) : return x

# time string to seconds conversion

re_ds = r"(?:(?P<d>\d+)\s*d)"
re_hs = r"(?:(?P<h>\d+)\s*h)"
re_ms = r"(?:(?P<m>\d+)\s*m)"
re_ss = r"(?:(?P<s>\d+)\s*s?)"

re_time = re.compile("^" + "?\s*".join((re_ds, re_hs, re_ms, re_ss))+"?$")

s2t = {"s" : 1}
s2t["m"] = 60 * s2t["s"]
s2t["h"] = 60 * s2t["m"]
s2t["d"] = 24 * s2t["h"]

def str2time(s):
    tm  = re_time.match(s.strip())
    if not (tm and tm.string) : raise "Invalid time string (%s)" % s
    return sum([int(ns) * s2t[f]
                for (f,ns) in zip("dhms", map(tm.group, "dhms")) if ns])
    
# Some list functions

def find(p, ible):
    for n,i in enumerate(ible):
        if p(i) : return True, n, i
    return False, -1, None

def exists(p, ible) :
    return find(p,ible)[0]

def index(p, ible):
    return find(p,ible)[1]

def first(p, ible):
    return find(p,ible)[2]

def nof(p, ible):
    return len(filter(p, ible))

def prod(lst): return reduce(operator.mul, lst, 1)

def unzip(lst) : return (map(fst,lst), map(snd,lst))
def zipWith(f, arglsts) : return [f(*args) for args in zip(*arglsts)]

def seqzip(lst):
    i1 = iter(lst)
    i2 = iter(lst); i2.next()
    return izip(i1,i2)
def ir2l(ir): return [i for i in ir] 

def normalize(lst):
    if lst == []: return []
    else:
        n = sum(lst)
        if n == 0: return lst
        else:      return [l/float(n) for l in lst]

def n_args_or_bust(args, casts=[], nmin=None, nmax = None):
    if not nmin : nmin = len(args.split())
    if not nmax : nmax = nmin
    if not nmin <= len(sys.argv)-1 <= nmax:
        print >>sys.stderr, "Usage %s" % sys.argv[0], args
        sys.exit(1)
    return castlist(sys.argv[1:],casts)

def argscall(f, args, casts=None, nmin=None, nmax = None):
    apply(f, n_args_or_bust(args, casts, nmin, nmax))

def genmain(ifns, ofns, fun, funargs):
    import pickle, types
    ifs = [file(ifn) for ifn in ifns]
    varc = max(map(pickle.load, ifs))
    ofs = [file(ofn,"w") for ofn in ofns]
    for of in ofs: pickle.dump(varc,of)
    for v in xrange(varc):
          picks = tuple([pickle.load(f) for f in ifs])
          ress = fun(*(picks+funargs))
          if isinstance(ress, DictType): ress = (ress,)
          for (res,of) in zip(ress, ofs): pickle.dump(res, of)
    for f in ifs + ifs : f.close()
    

def rowc(fn):
    f = open(fn, "r")
    c = 0
    for l in f.xreadlines() : c += 1
    f.close()
    return c

def colc(fn, sc=None):
    f = open(fn, "r")
    cc = [len(l.split(sc)) for l in f.xreadlines()]
    f.close()
    return cc

def table_by_rows(fn, sc=None):
    f = open(fn)
    table = [line[:-1].split(sc) for line in f.xreadlines()]
    f.close()
    return table

def table_by_cols(fn, cc, sc=None): # cc>1 please
    f = open(fn)
    table = [line[:-1].split(sc,cc-1) for line in f.xreadlines()]
    f.close()
    return [[(ci<len(r) and (r[ci],) or (None,))[0]\
            for r in table] for ci in range(cc)]

def cols_n_rest(fn, cc, sc=None):
    cnr = table_by_cols(fn,cc+1,sc)
    return cnr[:-1]+[[(r==None and ([],) or (r.split(sc),))[0]
                     for r in cnr[-1]]]

def col(fn, c, sc=None):
    f  = open(fn)
    cl = [line[:-1].split(sc)[c] for line in f.xreadlines()]
    f.close()
    return cl

def castlist(lst,casts):
    if type(casts) is BuiltinFunctionType:
        cl = repeat(casts,len(lst))
    elif type(casts) in (TupleType, ListType):
        if len(casts) > 0 :
            cl = chain(casts, repeat(casts[-1], len(lst) - len(casts)))
        else :
            cl = repeat(ident, len(lst))
    elif type(casts) is DictType:
        cl = [str]*len(lst)
        for k,ixs in casts.items():
            for ix in ixs:
                if type(ix) is IntType:
                    cl[ix] = k
                elif type(ix) is StringType:
                    cl[int(ix):] = [k]*(len(cl)-int(ix))
    else:
        cl = repeat(str,len(lst))
        
    return [c(e) for c,e in izip(cl,lst)]

def line2list(ln, sc, casts=None, cc=None):
    t = castlist(ln.split(sc), casts)
    return cc and (t[:cc] + [t[cc:]]) or t

def linen2list(ln, sc, casts=None, cc=None):
    return line2list(ln[:-1],sc,casts,cc)

def readvdf(vdfn):
    vdt = table_by_rows(vdfn,"\t")
    return [vdtr[0] for vdtr in vdt], [vdtr[1:] for vdtr in vdt]

def jess(vdfn):
    cc = colc(vdfn)
    return 0.5 * sum([c-1 for c in cc])

