#!/usr/bin/env python
from exceptions import Exception
from itertools import izip, ifilter, islice, tee

class UnknownDiscretizationCommand(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


def seqzip(iterable):
    a, b = tee(iterable)
    try:
        b.next()
    except StopIteration:
        pass
    return izip(a, b)

# EQW

def eqw(mi,ma,binc):
    range = ma == mi and  0.0001 or  float(ma - mi)
    return [mi + b * range/binc for b in xrange(1,binc)]
        

# NO HOLES EQW_NH

def ivs2divs(ivs):
    return [0.5*(b+c) for (a,b),(c,d) in seqzip(ivs)]

def full_ivs(binc, values):
    minv, maxv = values[0], values[-1]

    if binc <= 1 : return [minv, maxv]

    mdivsm   = [minv]+eqw(minv,maxv,binc)+[maxv]

    res = []

    abs = seqzip(mdivsm)
    a,b = abs.next()
    try:
        for v in values:
            if a<v and v<=b:
                res.append((a,b))
                a,b = abs.next()
    except:
        pass

    return res

def eqw_nh(bc, values):  return ivs2divs(full_ivs(bc, values))

# K-MEANS

def dists(v,means): return [abs(v-m) for m in means]

def minix(t): return t.index(min(t))

def kmeans(K,values,freqs):

    ivwidth = 1.0 * (values[-1] - values[0]) / K
    means   = [values[0] + ivwidth/2 + i * ivwidth for i in xrange(K)]
    oldgroups = [-1] * len(values)

    while True:
        
	# GROUP VALUES
	groups = [minix(dists(v,means)) for v in values]

	# CHECK CHANGE
        change = False
        for g,og in zip(groups,oldgroups):
            if g != og:
                change = True
                break

        if not change: break
            
        # NEW MEANS
        groupsums  = [0.0] * len(means)
        groupsizes = [0]   * len(means)
        for v,f,g in izip(values,freqs,groups):
            groupsizes[g] += f
            groupsums[g]  += f * v

        means = [gsum / gsize
                 for (gsum,gsize) in zip(groupsums, groupsizes)
                 if gsize > 0]
            
        oldgroups = groups[:]
            
    # DIVISION POINTS
    
    return [0.5 * (v1 + v2)
            for ((v1,g1), (v2,g2)) in seqzip(izip(values, oldgroups))
            if g1<g2]


def disp(ana, cmd_args):

    cmd, args = cmd_args[0], cmd_args[1:] 

    if cmd == 'AFTER':
        limit = int(args[0])
        if(ana["numvc"] <= limit):
            cmd, args = "NOM", None
        else:
            cmd, args = args[1], args[2:]

    dsp = {"ascvc":ana["ascvc"], "cmd":cmd}
    if cmd == 'EQW':
	dsp["divs"] = eqw(ana["min"], ana["max"], int(args[0]))
	dsp["binc"] = len(dsp["divs"]) + 1
    elif cmd == 'EQW_NH':
        nvals, freqs = zip(*ana["nvals"])
        numvals = map(float, nvals)
	dsp["divs"]    = eqw_nh(int(args[0]), numvals)
	dsp["binc"] = len(dsp["divs"]) + 1
    elif cmd ==  'DIS':
	dsp["divs"] = map(float, args)
	dsp["binc"] = len(dsp["divs"]) + 1
    elif cmd == 'NOM':
        if ana["min"] == ana["max"]:
	    dsp["divs"] = []
            dsp["binc"] = ana["numvc"] > 0 and 1 or 0
	else:
            nvals, freqs = zip(*ana["nvals"])
            numvals = map(float,nvals)
            avg = lambda (x,y) : 0.5 * (x+y)
            dsp["divs"] = map(avg, seqzip(numvals))
            dsp["binc"] = len(dsp["divs"]) + 1
    elif cmd == 'KM':
	if ana["max"] != ana["min"]:
            nvals, freqs = zip(*ana["nvals"])
	    dsp["divs"] = kmeans(int(args[0]), nvals, freqs)
	else:
	    dsp["divs"] = []
        dsp["binc"] = len(dsp["divs"]) + 1
    else: 
        raise UnknownDiscretizationCommand(cmd_args)

    return dsp

def dsp2line(dsp):
    return "%d\t%s" % (dsp['binc'], "\t".join(map(str, dsp['divs'])))

def line2dsp(line):
    t = line.split()
    return {'binc' : int(t.pop(0)), 'divs' : map(float, t)}
