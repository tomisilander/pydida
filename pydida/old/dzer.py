#!/usr/bin/env python
import sys
import os
import string
import re

if len(sys.argv) != 4:
	sys.stderr.write("Usage: dzer.py txtfile anafile cmdfile\n")
	sys.exit(1)

if not os.environ.has_key('BAYWAYHOME'):
	os.environ['BAYWAYHOME'] = "%s/bw" % os.environ['HOME']
	sys.stderr.write("Setting BAYWAYHOME = %s\n" % os.environ['HOME'])

txtfile, anafile, cmdfile = sys.argv[1:]
pid = os.getpid()

datfile = "/tmp/%d.dat" % pid
hstfile = "/tmp/%d.hst" % pid
vdfile  = "/tmp/%d.vd"  % pid

os.system("%s/bin/defcmd.pl %s %s" 
	% (os.environ['BAYWAYHOME'], anafile, cmdfile))

os.system("%s/bin/a2n.pl %s %s %s %s %s %s"
	% (os.environ['BAYWAYHOME'], anafile, txtfile, cmdfile, 
	   vdfile, hstfile, datfile))

spllines = map(lambda x: string.split(x[:-1], '\t'), open(anafile).readlines())
varnames = map(lambda x: x[0],  spllines)
vartypes = map(lambda x: x[1], spllines)
varmm    = map(lambda x: x[2:4], spllines)
valcount = map(lambda x: len(x[4:]), spllines)

cmdlines = open(cmdfile).readlines()

nummatch = re.compile('^\d+$')
eqwmatch = re.compile('^eqw\s\d+$')
divmatch = re.compile('^div')
fltmatch = re.compile('^-?\d+(?:\.\d+)?$')

prompt1 = "q=quit, a=all, number:\n";
prompt2 = "a=all, number, eqw <num>, div <divs>, n=nominal:\n";
prompt3 = "a=all:\n";

cmd = "a"
varno = None
while cmd != "q":
	if cmd=="a"  :
		for i in range(len(varnames)):
			print i,varnames[i],vartypes[i],varmm[i],valcount[i]
		varno = None
	elif nummatch.match(cmd):
		varno = int(cmd)

	if varno == None:
		cmd = raw_input(prompt1)
		continue

	if varno < 0 or varno >= len(varnames):
		print "Warning, illegal variable number", varno
		cmd = raw_input(prompt1)
		continue
	
	newcmd = None
	if cmd=="n":
		newcmd = "NOM\n"
	elif divmatch.match(cmd):
		if(vartypes[varno] == "A"):
			print "Cannot divide ascii values."
			cmd = "%d" % varno
			continue
		divs = string.split(cmd)[1:]

		if len(divs) <= 0:
			print "At least one divider needed."
			cmd = "%d" % varno
			continue

		oldf = None
		error = None
		for f in divs:
			if error: continue
			if(not fltmatch.match(f)):
				error = "%s is not proper division point" % f
				continue
			ff = float(f)
			if(oldf and oldf >= ff) : 
				error = "Wrong order: %f %f." % (oldf, ff)
				continue
			oldf = ff
		if error:
			print error
		else:
			newcmd = "DIS\t%s\n" % "\t".join(divs)
	elif eqwmatch.match(cmd):
		if(vartypes[varno] == "A"):
			print "Cannot divide ascii values."
			cmd = "%d" % varno
			continue
		eqs = string.split(cmd)[1]
		newcmd = "EQW\t%s\n" % eqs


	if(newcmd):
		cmdlines[varno] = newcmd;
		open(cmdfile,'w').writelines(cmdlines)
		os.system("%s/bin/a2n.pl %s %s %s %s %s %s"
		% (os.environ['BAYWAYHOME'], anafile, txtfile, cmdfile, 
   		   vdfile, hstfile, datfile))


	print varnames[varno], vartypes[varno], ":"
	print cmdlines[varno]
	print open(vdfile).readlines()[varno]
	print open(hstfile).readlines()[varno]

	cmd = raw_input(prompt2)
	

os.remove(datfile)
os.remove(hstfile)
os.remove(vdfile)
