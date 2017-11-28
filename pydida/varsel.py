from itertools import izip, count
import sys

import vars, varset, varcmd

def varsel(vnfile, datfile, vnfile_out, datfile_out,
           commands = '', cmd_file = None,
           **cmdsyntax):

    sx = varcmd.syntax(cmdsyntax)
    varnames = vars.vars(vnfile)
    vscmds   = varcmd.varscmds(varnames,commands,sx,cmd_file)
    vnf  = file(vnfile_out,"w")
    datf = file(datfile_out,"w")
    for (vl, dl, vcmds) in izip(file(vnfile), file(datfile), vscmds):
        if "in" in vcmds:
            vnf.write(vl)
            datf.write(dl)
    
if __name__ == "__main__":
    from coliche import che
    che(varsel,
        """
        vnfile   : the file containing one variable name per row
        datfile  : the file containing one variable per row
        vnfile-out
        datfile-out
        -f --cmd-file cmd-file : read commands from file first
        -c --cmd commands : separated by %s
        """ + varset.strusage + varcmd.strusage)
