#!/usr/bin/python2.4

import cgi;
import pydida.diz
import cfg, pervar
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
sid, sdir, sfn, wfn, cfn, sx = cfg.get_session(form)

######################### FORM INPUT ##########################

pvcmds = pervar.commands(sfn("pervar"), sx)

############################ ACTION  ##########################

pydida.diz.diz(sfn("vns"), sfn("dna"), wfn("ana"), sfn("typ"), sdir,
               commands  = pvcmds,
               cmd_file  = cfn,
               Imputation = None, # maybe some day not
               **sx)


######################### FORM OUTPUT ##########################

template, tproc = cfg.tmpl("dout", sid)

print "Content-Type: text/html\n"
print tproc.process(template)
