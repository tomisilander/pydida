from itertools import izip

import varset
import varcmd, vars
import sys

def mismark(vnfile, datfile, outfile, commands = '', cmd_file = None,
            miss_mark = "", **cmdsyntax):

    sx = varcmd.syntax(cmdsyntax)
    
    vns   = vars.vars(vnfile)
    cmds  = varcmd.prepend(sx, "miss "+miss_mark, commands)
    vscmds = varcmd.varscmds(vns, cmds, sx, cmd_file, ("miss",))
    
    outf = outfile == "-" and sys.stdout or file(outfile,"w")

    for (vcmds, dl) in izip(vscmds, file(datfile)): 
        acs = vcmds['miss']
        dt = (d.strip() not in acs and d.strip() or ""
              for d in dl[:-1].split("\t"))
        print >>outf, "\t".join(dt)

if __name__ == "__main__":
    from coliche import che
    che(mismark,
        """
        vnfile   : the file containing one variable name per row
        datfile  : the file containing one variable per row
        outfile  : datfile with missing values marked as empty
        -m --miss miss-mark : same as -c " .. :: miss miss-mark" : default ""
        -f --cmd-file cmd-file : read commands from file first
        -c --cmd commands : separated by %s 
        """ + varset.strusage + varcmd.strusage)
