import os
from itertools import imap, izip
import re
import vars, varcmd, datyp

cast = {'I' : int, 'F' : float,  'S' : str, 'M' : lambda x: None}

def tfields(l, tl):
    return (cast[t](field) for field, t in izip(l[:-1].split("\t"), tl))
    
nzeros=re.compile('[1-9]*')

def resolution(x):
    if type(x) is int:
        return pow(10,len(nzeros.split(str(x))[-1]))
    elif type(x) is float:
        return pow(10,-len(str(x).split('.')[1]))
    else:
        print 'resolution needs either int of float'

def analyne(l, tl, addvals):

    nvals, avals = {}, {}

    for t, field in imap(datyp.typify, addvals):
        if t in "S":
           avals[field] = 0
        elif t in "IF":
            nvals[field] = 0
            
    numc = sum(imap(lambda t: t in "IF", tl))
    ascc = sum(imap(lambda t: t == "S",  tl))
    misc = sum(imap(lambda t: t == "M",  tl))
    
    for tfield, t in izip(tfields(l, tl), tl[:-1]):
        if t in "IF":
            nvals[tfield] = nvals.get(tfield,0) + 1
        elif t == 'S':
            avals[tfield] = avals.get(tfield,0) + 1
                
    ana = {'numc'  : numc,
           'ascc'  : ascc,
           'misc'  : misc,
           'nvals' : nvals.items(),
           'avals' : avals.items(),
           'numvc' : len(nvals),
           'ascvc' : len(avals),
           'min'   : 0,
           'max'   : 0,
           'res'   : 0,
           }
    
    ana['nvals'].sort()
    ana['avals'].sort()

    if ana['numvc'] > 0 :
        ana['min'] = ana['nvals'][0][0]
        ana['max'] = ana['nvals'][-1][0]
        ana['res'] = min(resolution(v) for (v,c) in ana['nvals'])

    ana['type'] = ana['ascvc'] and ana['numvc'] and 'X' \
                  or ana['ascvc'] and 'A' \
                  or ana['numvc'] and 'N' \
                  or 'M'
    return ana

def dn(anafile) :
    return anafile+"_dir"

def fn(anafile, n) :
    return os.path.join(dn(anafile), str(n))

def save(ana, anafile):
    anaf = file(anafile, "w")
    for k_v in ana.iteritems():
        print >>anaf, k_v
    anaf.close()

def load(anafile):
    return dict(eval(line) for line in file(anafile))

def analynes(vnfile, datfile, typfile,
             commands = None, cmd_file = None, **cmdsyntax):

    sx = varcmd.syntax(cmdsyntax)
    vns = vars.vars(vnfile)
    vscmds   = varcmd.varscmds(vns,commands,sx,cmd_file,("addval","delval"))

    for (vcmds,dl,tl) in izip(vscmds, file(datfile), file(typfile)):
        yield analyne(dl, tl, vcmds.get('addval',[]))

def makeanadir(anafile):    
    adn = dn(anafile)
    if not os.path.exists(adn) or not os.path.isdir(adn):
        os.makedirs(adn)
    return adn

def datana(vnfile, datfile, typfile, anafile,
           commands = None, cmd_file = None, **cmdsyntax):

    makeanadir(anafile)
    
    anaf = file(anafile, "w")
    for i, lana in enumerate(analynes(vnfile, datfile, typfile,
                                      commands, cmd_file, **cmdsyntax)):
        afn = os.path.abspath(fn(anafile, i))
        save(lana, afn)
        print >>anaf, afn
    anaf.close()

def fanas(anafile):
    for line in file(anafile):
        yield load(line.strip())

# NEEDS MAIN
