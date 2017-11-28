#!/usr/bin/python

import sys
from string import *

def hugo(vdf, plaf, thtf, strf):
	print """
net
{
	node_size = (80 40);
	HR_Grid_X = "10";
    	HR_Grid_Y = "10";
	HR_Grid_GridSnap = "1";
    	HR_Grid_GridShow = "0";
	HR_Font_Name = "Arial";
	HR_Font_Size = "-12";
	HR_Font_Weight = "400";
	HR_Font_Italic = "0";
	HR_Propagate_Auto = "1";
}"""
	
	vdrows = map( lambda row: row[:-1], open(vdf).readlines())
	vdtable = map( lambda st: split( st, "\t") , vdrows)
	nodenames = map(lambda row: row[0], vdtable)
	nodevals  = map(lambda row: row[1:], vdtable)
	plarows = open(plaf).readlines()[:1+len(nodenames)];
	pladim = split(plarows[0])[2:4]
	nodepositions= map( lambda st: split( st, " " )[3:5] , plarows[1:]) 

	for i in range(len(nodenames)):
		vl = map(lambda x: "\"%s\"" % x, nodevals[i]);
		x = int(float(nodepositions[i][0]) * 750 / float(pladim[0]));
		y = int(float(nodepositions[i][1]) * 550 / float(pladim[1]));
		print """
node V_%d
{
    states = (%s);
    label = "%s";
    position = (%d %d);
}""" % (i, join(vl), nodenames[i], x, y)


	thtfile = open(thtf)
	strfile = open(strf)
	strfile.readline()
	for i in range(len(nodenames)):

		thtbl=[]
		for l in range(int(thtfile.readline())):
			thtbl.append(thtfile.readline())

		parents = map(lambda x: "V_%s" % x, split(strfile.readline())[2:])
                parents.reverse();
		prs = " ";
                if parents:
			prs = " | " + join(parents, " ")

		print """
potential ( V_%d%s)
{
    data = (%s);
}""" % (i, prs, join(thtbl,""))

hugo(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])








