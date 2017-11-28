#!/usr/bin/python2.4

import os, cgi;
import cfg, pervar, fileup

import cgitb; cgitb.enable()

form = cgi.FieldStorage()
sid, sdir, sfn, wfn, cfn, sx = cfg.get_session(form)


######################### FORM INPUT ##########################

opts=[]

def handle_names():
    names = form.getfirst("names")
    if names == "FILE":
        namefn = sfn("vns.raw")
        if fileup.save(form, 'vnfile', namefn):
            return namefn
        else:
            cfg.error("Could not upload variable name file!")
    else:
        return names

opts.append(("--delim",    form.getfirst("delim")))
opts.append(("--names",    handle_names()))
opts.append(("--start",    form.getfirst("start")))
opts.append(("--miss" ,    form.getfirst('missmark')))
opts.append(("--rowise",   form.getfirst("rowise") == "yes"))
opts.append(("--cmd-file", cfn))
opts.extend(cfg.sx_options(sx))

############################ ACTION  ##########################

cfg.save_cmds(cfn, form.getfirst("cmd_file"))

pargs = " ".join((sfn("dat.org"), sdir))
cmd   = "python2.4 pydida/din.py %s %s" % (pargs, cfg.optcat(*opts))
# raise cmd
to_cmd, from_cmd, cmderr = os.popen3(cmd)
err = cmderr.read()
ok  = (not err) and int(from_cmd.readline())

######################### FORM OUTPUT ##########################

if ok:
    pervar.create_cmds(len(cfg.vars(sdir)), sfn("pervar")).close()
    print "Location: /cgi-bin/anas.py?sid=%s&action=First\n" % sid
else:
    if err:
        cfg.error(err, sid)
    else:
        cfg.error(from_cmd.read(), sid)
