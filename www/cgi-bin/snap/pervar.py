import shelve
import pydida.varcmd

def get_cmds(filename, wb=False):
    return shelve.open(filename, writeback=wb)

def varcommands(i, cmds, sx=pydida.varcmd.syntax({})):
    vcmds = (pydida.varcmd.build_cmd(cmd+" "+args, sx, str(i))
             for (cmd,args) in cmds[str(i)].items())
    return pydida.varcmd.join(sx, *vcmds)

def commands(filename, sx=pydida.varcmd.syntax({})):
    cmds = get_cmds(filename)
    return pydida.varcmd.join(sx, *(varcommands(i, cmds, sx)
                                    for i in cmds if cmds[i]))
    
def create_cmds(nof_vars, filename, defcmds={}):
    cmds = get_cmds(filename, wb=True)
    for vix in xrange(nof_vars):
        cmds[str(vix)] = defcmds.copy()
    return cmds
