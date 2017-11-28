#!/usr/bin/python2.4

import cgi, shutil, os
from itertools import izip, count
from pydida import datana, varcmd
import cfg, pervar
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
sid, sdir, sfn, wfn, cfn, sx = cfg.get_session(form)

action = form.getfirst("action")

anafn  = sfn("ana")
wanafn = wfn("ana")
anadn  = datana.dn(anafn)
wanadn = datana.dn(wanafn)
    

if action == "First":

    shutil.copyfile(anafn, wanafn)
    if os.path.exists(wanadn): shutil.rmtree(wanadn)
    shutil.copytree(anadn, wanadn)
    
elif action == "Apply":

    # GET COMMANDS, SAVE THEM AND ANALYZE ALL
    
    cfg.save_cmds(cfn, form.getfirst("cmd_file",''))

    datana.datana(sfn("vns"),
                  sfn("dna"),
                  sfn("typ"),
                  wanafn,
                  pervar.commands(sfn("pervar"), sx),
                  cfn,
                  **sx)

elif action == "Proceed":

    # could check that pervar and commands 
    
    print "Location: /cgi-bin/diz.py?sid=%s\n" % sid
    sys.exit()

else:
    pass


# NOW SHOW THE RESULTS

template, tproc = cfg.tmpl("anas", sid)

tproc.set('cmd_file', file(cfn).read())

anas = datana.fanas(wanafn)
vns  = cfg.vars(sdir)

pvscmds = pervar.get_cmds(sfn("pervar"))

def banas():
    anakeys = "name vix min max numvc ascvc misc type cmd".split()
    for vix, a, vn in izip(count(), anas, vns):
        pvcmds = pvscmds[str(vix)]
        vcmds = [cmd +" " +pvcmds[cmd]
                 for cmd in ('addval', 'delval', 'DIS', 'IMP')
                 if cmd in pvcmds]
        a['name'] = vn
        a['vix']  = vix
        a['cmd']  = varcmd.join(sx, *(vcmds))

        yield dict(zip(anakeys, map(a.get, anakeys)))

tproc.set('Anas', list(banas()))

print "Content-Type: text/html\n\n"
print tproc.process(template)
