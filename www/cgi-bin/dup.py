#!/usr/bin/python2.4

import cgi
import cfg, fileup, pydida.varcmd

import cgitb; cgitb.enable()

form = cgi.FieldStorage()
sid, sdir, sfn, wfn, cfn, sx = cfg.create_session()

# Update Syntax

for k in "rng_mark sep_mark var_cmd_sep cmd_sep".split():
    v = form.getfirst(k,'').strip()    
    sx[k] = v and v or sx[k] # Not good - fail hard
cfg.set_syntax(sdir, sx)

cmds  = pydida.varcmd.build_cmds(sx=sx)
cfg.save_cmds(cfn, cmds.replace(sx['cmd_sep'],"\n"))

# Upload data file

if not fileup.save(form, "datafile", sfn("dat.org")):
    cfg.error("Empty file recieved!", sid)


template, tproc = cfg.tmpl("din.tmpl", sid)
tproc.set('cmd_file', file(cfn).read())
print "Content-Type: text/html\n"
print tproc.process(template)
