#!/usr/bin/python2.4

import sys, cgi
from itertools import islice

import cfg, pervar
from pydida import varcmd, diz, datana

import cgitb; cgitb.enable()

def num_freqs(nvals, tproc, nof_ivs):

    mi, ma = min(nvals)[0], max(nvals)[0]
    rng = (ma-mi)
    eps = 0.01 * rng
    
    ilen = (ma - mi + eps) / nof_ivs

    bix = lambda x: int((x-mi-eps/2)/ilen)

    freqs = [0]*nof_ivs
    for x,f in nvals: freqs[bix(x)] += f

    maxfreq = max(freqs)
    heights = [f*100.0/maxfreq for f in freqs]

    coords = [mi-ilen/2 + c * ilen for c in xrange(len(freqs)+1)]

    tproc.set("Heights",  [{'freq' : f, 'height': h}
                           for f,h in zip(freqs, heights)])

    tproc.set("Coords", [{'coord': "%.2f" % c} for c in coords])
    tproc.set("Axis",   range(2*len(coords)))

    return maxfreq

def asc_freqs(avals, tproc, mxfrq=-1):
    coords, freqs = zip(*avals)
    maxfreq = max(freqs+(mxfrq,))
    heights = [f*100.0/maxfreq for f in freqs]
    
    tproc.set("Heights_a",  [{'freq' : f, 'height': h}
                             for f,h in zip(freqs, heights)])
    
    tproc.set("Coords_a", [{'coord' : c } for c in coords])
    tproc.set("Axis_a",   range(len(coords)))


nth = lambda i, n : islice(i,n,n+1).next()

######################## FORM INPUT ##################

form = cgi.FieldStorage()
sid, sdir, sfn, wfn, cfn, sx = cfg.get_session(form)
vix       = int(form.getfirst("vix",0))
vns       = cfg.vars(sdir)


# READ COMMANDS FROM PERVAR OR FORM

form2cmd = {'addval' : 'addval',
            'delval' : 'delval',
            'dzcmd'  : 'DIS',
            'impcmd' : 'IMP'}

cmd_args = {}

if form.getfirst("action") not in ("Test", "Accept"):
    pvcmds = pervar.get_cmds(sfn("pervar"), wb=True)[str(vix)]
    for fcmd, cmd in form2cmd.iteritems():
        if cmd in pvcmds:
            cmd_args[cmd] = pvcmds.get(cmd).strip()
else:
    for fcmd, cmd in form2cmd.iteritems():
        if form.has_key(fcmd):
            cmd_args[cmd] = form.getfirst(fcmd).strip()
        

# ACT ON ACCEPT AND RELOCATE

if form.getfirst("action") == "Accept":

    # store commands

    pvscmds = pervar.get_cmds(sfn("pervar"), wb=True)
    pvscmds[str(vix)] = cmd_args
    pvscmds.close()
    
    print "Location: /cgi-bin/anas.py?sid=%s\n" % sid
    sys.exit()


# ACT ON PREANALYSIS COMMANDS

def cmds2command(cmds):
    command = ""
    for cmd in cmds:
        if cmd in cmd_args:
            args = cmd_args[cmd]
            command = varcmd.prepend(sx, cmd+" "+args, command, vix)
    return command

if 'addval' in cmd_args or 'delval' in cmd_args:
    dl     = nth(file(sfn("dna")), vix)
    tl     = nth(file(sfn("typ")), vix)    
    cmds   = ("addval","delval")
    advcmd = varcmd.varscmds(vns, cmds2command(cmds), sx, cfn, cmds)[vix]
    ana    = datana.analyne(dl, tl, advcmd.get('addval', []))
else:
    anafn = datana.fn(wfn("ana"), vix)
    ana   = datana.load(anafn)


# SET TEMPLATE VARIABLES FOR ANALYSIS

template, tproc = cfg.tmpl("ana", sid)

tproc.set('addval', cmd_args.get('addval', ''))
tproc.set('delval', cmd_args.get('delval', ''))

tproc.set("baruri", "black.png")
tproc.set("vix", vix)
tproc.set('name', cfg.vars(sdir)[vix])

prelimit = int(form.getfirst("prelimit",6))
prebins  = int(form.getfirst("prebins",16))
has_numbers = ana['numvc'] > 1

tproc.set('prelimit',  prelimit)
tproc.set('prebins',   prebins)

tproc.set("has_numbers", int(has_numbers))

if has_numbers and (ana['numvc'] + ana['ascvc'] > prelimit):
    tproc.set("numfreqs", 1)
    mxfrq = num_freqs(ana['nvals'], tproc, prebins)
    if ana['avals']: asc_freqs(ana['avals'], tproc, mxfrq)
else:
    tproc.set("nomfreqs", 1)
    asc_freqs(ana['avals']+ana['nvals'], tproc)


### POST DISCRETIZATION ###

### ACT DIZ AND IMP ###
    
outfs = dict((fn, file(wfn(fn), "w"))
             for fn in "dsp vds hst dzd".split())

positive = ("DIS", "IMP")
vcmd = varcmd.varscmds(vns, cmds2command(positive), sx, cfn, positive)[vix]

diz.lin(vns[vix],
        nth(file(sfn("dna")),vix),
        ana,
        nth(file(sfn("typ")), vix),
        vcmd.get('DIS', ""),
        vcmd.get('IMP', None),
        outfs)

for f in outfs.values(): f.close()

# SET TEMPLATE VARIABLES FOR POST DISCR

vds  = file(wfn('vds')).read().strip().split("\t")[1:]
frqs = map(int, file(wfn('hst')).read().strip().split())

tproc.set("Dloop",[{'vd' : vd, 'freq' : frq, 'height' : 100*frq/max(frqs)}
                       for (vd, frq) in zip(vds, frqs)])

tproc.set("dzcmd",  cmd_args.get('DIS',''))
tproc.set("impcmd", cmd_args.get('IMP',''))

######################## FORM OUTPUT ##################

print "Content-Type: text/html\n\n"
print tproc.process(template)
