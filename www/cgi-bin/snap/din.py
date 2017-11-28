#!/usr/bin/python2.4

import os, cgi;
from itertools import izip
import pydida.datana
import cfg, pervar, fileup

import cgitb; cgitb.enable()

form = cgi.FieldStorage()
sid, sdir, sfn, wfn, cfn, sx = cfg.get_session(form)


######################### FORM INPUT ##########################

args = sx.copy()

### SEPARATOR ###

sepname = {"TAB": "\t", "SPACE":" "}

sep = form.getfirst("separator", "WS")
if sep == "single":
    sepchar = form.getfirst("sepchar", "SPACE")
    args['delim'] = sepname.get(sepchar, sepchar)

### NAMES ###

names = form.getfirst("names", "ROW")

if names == "ROW":
    # args['names'] = "1" # Hmm
    pass
elif names== "GEN":
    args['names'] = "GEN"
    try:
        args['start'] = int(form.getfirst("start", "0"))
    except:
        raise
else:
    args['names'] = sfn("vns.raw")
    if not fileup.save(form, 'vnfile', args['names']):
        cfg.error("Could not upload variable name file!")

### MISSING ###

missmark = form.getfirst('missmark','').strip()
if missmark:
    args['missmark'] = missmark

### ROWISE ###

args['rowise'] = form.getfirst("rowise", "no") == "yes"

### Variable processing commands ###

cfg.save_cmds(cfn, form.getfirst("cmd_file", ""))
args['cmd_file'] = cfn

############################ ACTION  ##########################

import pydida.din
import pydida.formatcheck

datafile = sfn("dat.org")

ok, nof_rows, nof_cols, msg = pydida.din.din(datafile, sdir, **args)

######################### FORM OUTPUT ##########################

if ok:
    pervar.create_cmds(len(cfg.vars(sdir)), sfn("pervar")).close()
    print "Location: /cgi-bin/anas.py?sid=%s&action=First\n" % sid
else:
    cfg.error(msg, sid)
