#!/usr/bin/python2.4

import cgi, sys
import pydida.dout
import cfg, pervar

import cgitb; cgitb.enable()

form = cgi.FieldStorage()
sid, sdir, sfn, wfn, cfn, sx = cfg.get_session(form)

######################### FORM INPUT ##########################

args = {}

### SEPCHAR ###

sepchar = form.getfirst("sepchar", 'NONE').strip()
delim = {'TAB': "\t", 'SPACE' : ' ', 'NONE' : ''}.get(sepchar, sepchar)
args['Delim'] = delim

### NAMES ###

names = form.getfirst("names", 'ROW') # should check
args['Names'] = names

### MISSMARK ###

missmark = form.getfirst("missmark", '')
missmark = {'TAB': "\t", 'SPACE' : ' ', 'NONE' : ''}.get(missmark, missmark)
args['Missmark'] = missmark

### ROWISE ###

rowise = form.getfirst("rowise", False)
args['Rowise'] = rowise=="yes"

### EOL-TYPE ###

eol_type = form.getfirst("eol_type", 'UNIX')
args['EOL_type'] = eol_type # should check

# now one could check syntax better

############################ ACTION  ##########################

pydida.dout.dout(sfn("vds"), sfn("dzd"), sdir, **args)


pvcmds = pervar.commands(sfn("pervar"), sx).replace(sx['cmd_sep'],"\n")
file(sfn("cmd"),"w").write(file(cfn).read()+"\n"+pvcmds)


######################### FORM OUTPUT ##########################

template, tproc = cfg.tmpl("results", sid)

print "Content-Type: text/html\n"
print tproc.process(template)
