#!/usr/bin/env python
from datana         import tfields, fanas
from dispoint       import disp, dsp2line
from adis2vd        import vald
from adis2dat       import dat, hst
from impute         import impute

from itertools      import izip, imap, count
import varset, varcmd, vars

import os

def lin(vn, l, ana, tl, dzcmd, impcmd, use_limits, outfs):
    
    dsp = disp(ana, dzcmd)
    vd  = vald(vn, ana, dsp, use_limits)
    nfields = dat(vd, ana, dsp, tfields(l, tl))
    freqs   = hst(nfields, vd)
    if ana['misc'] and impcmd:
        nfields = impute(nfields, freqs, impcmd)
        freqs   = hst(nfields, vd)
    
    print >>outfs["dsp"], dsp2line(dsp)
    print >>outfs["hst"], "\t".join(map(str, freqs))
    print >>outfs["dzd"], "\t".join(imap(str, nfields))
    print >>outfs["vds"], "%s\t%s" % (vd['name'], "\t".join(vd['vds']))


def diz(vnfile, dfn, anafile, typfile, resdn,
        commands      = "",  cmd_file      = None,
        Imputation    = None, Limits = False,
        **sx ):

    diradd = lambda x : os.path.join(resdn, x)

    outfs = {}
    for outfn in "dsp vds hst dzd".split():
        outfs[outfn] = file(diradd(outfn),"w")

    vns = vars.vars(vnfile)
    sx = varcmd.syntax(sx)

    if Imputation:
        commands = varcmd.prepend(sx, "IMP %s" % Imputation, commands)

    positive = ("DIS","IMP", "addval", "delval")
    vscmds = varcmd.varscmds(vns, commands, sx, cmd_file, positive)

    for (vn, vcmd, l, ana, tl) in izip(vns, vscmds, file(dfn),
                                       fanas(anafile), file(typfile)):
        lin(vn, l, ana, tl, vcmd['DIS'], vcmd.get('IMP', None), Limits, outfs)


strusage = """
-I --Imputation Imputation : only GI supported this far
-L --Limits (bool) : include min and max in value intervals: default: False
"""

if __name__ == "__main__":
    import sys
    from coliche import che
    
    diz_strusage = ("""
    vnfile
    datafile
    anafile
    typefile
    result_dir
    """
    + strusage
    + """
    -c --cmd commands      : in quotes
    -f --cmd-file cmd-file : read commands from file first
    """ + varset.strusage + varcmd.strusage)

    che(diz, diz_strusage)
    resdir = che(lambda *ps, **ks: ps[4], diz_strusage)
    print >>file(os.path.join(resdir, "diz.cmd"), "w"), " ".join(sys.argv)
