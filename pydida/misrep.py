from itertools import izip

import varset, vars
import varcmd
import sys

def misrep(vnfile, datfile, repfile, commands = None, cmd_file = None,
           miss_mark = "", **cmdsyntax):

    sx = varcmd.syntax(cmdsyntax)
    vns = vars.vars(vnfile)
    cmds  = varcmd.prepend(sx, "miss "+miss_mark, commands)
    vscmds = varcmd.varscmds(vns, cmds, sx, cmd_file, ("miss",))

    repf = repfile == "-" and sys.stdout or file(repfile,"w")

    for (vcmds, dl) in izip(vscmds, file(datfile)):
        acs = vcmds['miss']
        nof_mvals = sum(int(d.strip() in acs)
                        for d in dl[:-1].split("\t"))
        print >>repf, nof_mvals

if __name__ == "__main__":
    from coliche import che
    che(misrep,
        """
        vnfile   : the file containing one variable name per row
        datfile  : the file containing one variable per row
        repfile  : reports number of missing values per variable
        -m --miss miss_mark : same as -c " .. :: miss miss-mark" : default ""
        -f --cmd-file cmd-file : read commands from file first
        -c --cmd commands : separated by %s 
        """ + varset.strusage + varcmd.strusage)
