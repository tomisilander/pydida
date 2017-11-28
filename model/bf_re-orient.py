#!/usr/bin/python

import sys, random, os

if len(sys.argv) != 3:
    print >>sys.stderr,\
          "Usage: %s strfile_in strfile_out" % sys.argv[0]
    sys.exit(1)

str_fn_in, str_fn_out= sys.argv[1:]

# load the net

istrf = open(str_fn_in, "r")
nodecount = int(istrf.readline())
net = [([],[]) for i in range(nodecount)]
for i in range(nodecount):
    ps = map(int, istrf.readline().split()[2:])
    net[i][0].extend(ps)
    for p in ps: net[p][1].append(i)    
istrf.close()
#print net

def anc_to_dec(net, i):
#    print "anc_to_dec", i, net[i][0]
#    print net
    for p in net[i][0]:
        anc_to_dec(net, p)

        net[i][0].remove(p) # Remove p from i's parents 
        net[i][1].append(p) # and to its children
        net[p][1].remove(i) # Remove i from p's children
        net[p][0].append(i) # and add it to its parents

#    print "out anc_to_dec", i, net[i][0]
#    print net

def delics(ornodes, net, i):
    ornodes.remove(i)
    for c in net[i][1]:
        delics(ornodes, net, c)

ornodes = list(range(nodecount))
while ornodes:
    i = random.choice(ornodes)
#    print "chose",i
    anc_to_dec(net,i)
#    print net
    delics(ornodes,net,i)

ostrf = open(str_fn_out,"w")
print >>ostrf, nodecount
for pl,cl in net:
    print >>ostrf, len(cl), len(pl), " ".join(map(str,pl))
ostrf.close()
