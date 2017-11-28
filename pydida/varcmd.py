from itertools import imap
import varset, vars

cmd_sep = ";"
var_cmd_sep = "::"

def syntax(args):
    sx = {'cmd_sep'     : args.get('cmd_sep', cmd_sep),
          'var_cmd_sep' : args.get('var_cmd_sep', var_cmd_sep)}
    sx.update(varset.syntax(args))
    return sx


cmd_defaults = ("in", "DIS AFTER 6 EQW 4", "mis ")

def join(sx, *cmds):
    return sx['cmd_sep'].join(cmds)

def build_cmd(cmd, sx=syntax({}), sel=None):
    if sel == None: sel = sx['rng_mark']
    return (" "+sx['var_cmd_sep']+" ").join((str(sel), cmd))
    
def prepend(sx, cmd, cmds, sel=None):
    if sel == None: sel = sx['rng_mark']
    return join(sx, build_cmd(cmd, sx, sel), cmds)

def build_cmds(cmds = cmd_defaults,
               sx   = syntax({}),
               sels = None):
    if sels == None: sels = [sx['rng_mark']]*len(cmds)
    return join(sx, *map(build_cmd, cmds, [sx]*len(cmds), sels))

def lines2cmds(lines, sx=syntax({})):
    return lines.replace("\n",sx['cmd_sep'])

def cascade(cmds="", cmdfile=None, sx=syntax({})):
    return join(sx,
                build_cmds(sx=sx),
                lines2cmds(cmdfile and file(cmdfile,"rU").read() or "", sx),
                lines2cmds(cmds, sx))

def setcmds(varnames, cmds, sx=syntax({}), positives = "ALL"):
    
    for cmdl in imap(str.strip, cmds.split(sx['cmd_sep'])):
        if "#" in cmdl:
            cmdl, comment = map(str.strip, cmdl.split("#",1))

        if not cmdl: continue
        vs_expr, cmd = map(str.strip, cmdl.split(sx['var_cmd_sep'], 1))
        args = cmd.split()
        cmd = args.pop(0)
        if positives == "ALL" or cmd in positives:
            vs = varset.varset(vs_expr, varnames, **sx)
            yield (vs, cmd, args)


def def_action(res, cmd, acs): res[cmd] = acs
def out_action(res, cmd, acs):
    if 'in'  in res: del res['in']
def OUT_action(res, cmd, acs):
    if 'OUT' in res: del res['OUT']

def miss_action(res, cmd, acs):
    if acs:  def_action(res,cmd,acs)
    else:   res[cmd] = ['']

def addval_action(res, cmd, acs):
    avs = res.setdefault('addval',[])
    for a in acs:
        if not a in avs:
            avs.append(a)

def delval_action(res, cmd, acs):
    avs = res.setdefault('addval',[])
    for v in acs:
        if v in avs:
            avs.remove(v)
            
actions = {'out'    : out_action,
           'miss'   : miss_action,
           'addval' : addval_action,
           'delval' : delval_action,
           'OUT'    : OUT_action,
           }

def varscmds(varnames, cmds, sx=syntax({}), cmdfile=None, positives = "ALL"):

    if not cmds or isinstance(cmds, str):
        cmds = cascade(cmds, cmdfile, sx=sx)
        cmds = setcmds(varnames, cmds, sx, positives)

    cs = [{} for vn in varnames]
    for (vs, cmd, acs) in cmds:
        for v in vs:
            actions.get(cmd, def_action)(cs[v], cmd, acs)
    return cs


        
strusage = """
--cmd-sep   cmd-sep       : separator for commands: default "\%s"
--var-cmd-sep var-cmd-sep : token to separate vars and command: default "%s"
        """ % (cmd_sep, var_cmd_sep)

# JUST TO TEST

if __name__ == "__main__":

    from coliche import che

    def main(vnfile, commands="", cmd_file=None, **sx):
        sx = syntax(sx)
        vns = vars.vars(vnfile)
        for t in varscmds(vns, commands, sx, cmd_file):
            print t
            
    che(main,
        """
        vnfile          : one variable name per row 
        -f --cmd-file cmd-file : read commands from file first
        -c --cmd commands : separated by %s
        """ + strusage)
