#!/usr/bin/python2.4

import cgi, os
import pydida.diz
import cfg, pervar
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
sid, sdir, sfn, wfn, cfn, sx = cfg.get_session(form)

######################### FORM INPUT ##########################

pvcmds = pervar.commands(sfn("pervar"), sx)

############################ ACTION  ##########################

pargs = " ".join((sfn("vns"), sfn("dna"), wfn("ana"), sfn("typ"), sdir))
opts  = [("--cmd-file", cfn), ("--cmd", pvcmds)] + cfg.sx_options(sx)
cmd   = "python2.4 pydida/diz.py %s %s" % (pargs, cfg.optcat(*opts))

to_cmd, from_cmd, cmderr = os.popen3(cmd)
err = cmderr.read()

######################### FORM OUTPUT ##########################

if err:
    cfg.error(err, sid)
else:        
    template, tproc = cfg.tmpl("dout", sid)

    print "Content-Type: text/html\n"
    print tproc.process(template)
