#!/usr/bin/python2.4

import cgi, sys
import cfg

import cgitb; cgitb.enable()

form = cgi.FieldStorage()
sid, sdir, sfn, wfn, cfn, sx = cfg.get_session(form)
fn = form.getfirst("fn", False)

print "Content-Type: text/plain\n"
for l in file(cfg.sfn(sdir, fn)):
    sys.stdout.write(l)
