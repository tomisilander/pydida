#!/usr/bin/python
from bwutil import *
import math

fns = n_args_or_bust(5,"nbtht githt nbsb gisb nbatht")
files =(nbthtf,githtf,nbsbf,gisbf,nbathtf)= map(open,fns,("r","r","r","r","w"))

gisb = map(float, gisbf.readlines())
nbsb = map(float, nbsbf.readlines())

def weights(x,y):
	if(x-y)>200:
		return (1.0,0.0)
	elif(x-y) < -200:
		return (0.0,1.0)
	else:
		r = math.exp(x-y)
		yw = 1.0 / (r + 1.0)
		xw = 1.0-yw
		return (xw,yw)

wghts = zipWith(weights, (nbsb, gisb))

def nbatht(nbtht,githt,nbw,giw): 
	return [nbw*nbth + giw*gith for (nbth,gith) in zip(nbtht,githt)]

githtls = githtf.readlines()
vix = 0
for i in range(1,len(githtls), 2):
	nbw, giw = wghts[vix]
	githt = map(float,linen2list(githtls[i]," "))
	
	pc = int(nbthtf.readline())
	print >>nbathtf, pc
	for j in range(pc):
		nbtht  = map(float,linen2list(nbthtf.readline()," "))
		print >>nbathtf, " ".join(map(str,nbatht(nbtht,githt,nbw,giw)))
	vix += 1

method_mapply(files, "close")


