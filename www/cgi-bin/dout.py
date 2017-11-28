#!/usr/bin/python2.4

import cgi, os
import cfg, pervar

import cgitb; cgitb.enable()

form = cgi.FieldStorage()
sid, sdir, sfn, wfn, cfn, sx = cfg.get_session(form)

######################### FORM INPUT ##########################

opts = []

opts.append(('--Delim',    form.getfirst("sepchar")))
opts.append(('--Names',    form.getfirst("names")))
opts.append(('--Miss',     form.getfirst("missmark")))
opts.append(('--Rowise',   form.getfirst("rowise")=="yes"))
opts.append(('--EOL-type', form.getfirst("eoltype")))
# opts.append(('--cmd-file', cfn))
# opts.extend(cfg.sx_options(sx))

############################ ACTION  ##########################

## Build cmd

eolify = lambda s : s.endswith("\n") and s or (s and (s+"\n") or s)
fcmds  = file(cfn).read()
pvcmds = pervar.commands(sfn("pervar"), sx).replace(sx['cmd_sep'],"\n")
file(sfn("cmd"),"w").write("".join(map(eolify, (fcmds, pvcmds))))

## Call dout

pargs = " ".join((sfn("vds"), sfn("dzd"), sdir))
cmd = "python2.4 pydida/dout.py %s %s" % (pargs, cfg.optcat(*opts))

#raise cmd

to_cmd, from_cmd, cmderr = os.popen3(cmd)
err = cmderr.read()

## Build options

if not err:
    optlines = "".join(file(sfn(dxx)).read().replace(sdir, "res_dir")
                       for dxx in ("din.cmd", "diz.cmd", "dout.cmd"))
    file(sfn("opt"), "w").write(optlines)

######################### FORM OUTPUT ##########################

if err:
    cfg.error(err, sid)
else:
    template, tproc = cfg.tmpl("results", sid)
    print "Content-Type: text/html\n"
    print tproc.process(template)
