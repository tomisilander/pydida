#!/usr/bin/python

from optparse import OptionParser

import sys


# A simple command line parser based on definition string
# - the idea is to check the command line against
#   the given definition and if it is ok, return a dictionary
#   that can be passed as an argument to the function


casts = {"int"   : int,
         "float" : float,
         "bool"  : bool,
         "str"   : str} # other??


def is_option(t):
    return t and t.startswith("-") and len(t)>1

def is_posarg(t):
    return t and not is_option(t) 

def is_cast(t):
    return t and t.startswith("(") and t.endswith(")")

def is_choice(t):
    return t and "|" in t

def is_assignment(t):
    return t and (t.find("->") >= 0)




def handle_option(parser, optdef):
    opt, help = (":" in optdef) and optdef.split(":",1) or (optdef,"")
    optstrings =  []
    optatts    =  {"help" : help.strip(), "nargs":0}

    for term in opt.split():
        if is_option(term):
            optstrings.append(term)
        elif is_cast(term):
            optatts["type"] = term[1:-1]
        elif is_assignment(term):
            const, dest = term.split("->")
            optatts["dest"]  = dest
            optatts["const"] = const
        elif is_choice(term):
            optatts["choices"] = term.split("|")
        else:
            optatts["dest"]   = term
            optatts["nargs"]  = 1

    # Set default type
    
    if "type" not in optatts:
        if not optatts["nargs"]:
            optatts["type"] = "int"

    # Eval const

    if "type" in optatts and "const" in optatts:
        optatts["const"] = eval("%(type)s(%(const)s)" % optatts)

    # Set action

    if optatts["nargs"]:
        optatts["action"] = "store"
    else:
        optatts["action"] = "store_const"
        if not "dest" in optatts:
            optatts["const"] = True
        del optatts["type"]
        del optatts["nargs"]
    
    # Finally

    parser.add_option(*(optstrings),**(optatts))
            


def handle_posarg(pargdef):
    parg, help = (":" in pargdef) and pargdef.split(":",1) or (pargdef,"")
    cast = "str"
    name = ""
    for term in parg.split():
        if is_cast(term):
            cast= term[1:-1]
        else:
            name = term

    return (name, cast, help.strip())


def pargs_n_opts(optdefs):

    pargs = map(handle_posarg, filter(is_posarg, optdefs))

    # based on pargs, build usage string
    
    usage = "%prog [options]"

    if pargs:
        usage += " "
        usage += " ".join([parg[0] for parg in pargs])

        # add explanation for pargs if any of them has helptext

        hpargs = filter(lambda parg: str.strip(parg[2]), pargs)

        if hpargs:
            usage += " \n\narguments:"
        
            for (name, type, help) in pargs:
                usage += "\n  %s %s" % (name.ljust(12), help)
            

    # then parse option definitions
    
    parser = OptionParser(usage=usage)

    for optdef in filter(is_option, optdefs):
        handle_option(parser, optdef)

    return pargs, parser



def che(func, optdefs):

    # to allow semicolons with syntax \;
    
    optdefs = optdefs.replace("\;", "@@@@semicolon@@@@");
    optdefs = optdefs.replace(";","\n")
    optdefs = optdefs.replace("@@@@semicolon@@@@", ";");

    lines = map(str.strip, optdefs.split("\n"))
    pargs, parser = pargs_n_opts(lines)

    sysargs = sys.argv[1:]

    # rip non-option negative numbers from sysargs and remember arg positions
    # so that later negative numbers can be re-inserted to cargs
    # to correct places
    
    argposs = dict([(a,i) for (i,a) in enumerate(sysargs)])

    negargs, nonnegargs, takes_value = [],[], False
    for a in sysargs:
        o = parser.get_option(a)
        if o == None:
            try:
                if float(a)<0 and not takes_value:
                    negargs.append(a)
                    takes_value = False
                    continue
            except:
                pass
            takes_value = False
        else: # a is an option
            takes_value = o.takes_value()
            
        nonnegargs.append(a)

    opts, cargs = parser.parse_args(nonnegargs)

    cargs.extend(negargs) # let us reinsert the negargs and sort
    cargs.sort(lambda x,y : cmp(argposs[x],argposs[y]))
    
    if len(cargs) != len(pargs):
        parser.print_help()
        if cargs:
            sys.exit("\nERROR: wrong number of arguments")
        else:
            sys.exit()

    # Now we go through command line args and set up the list of args

    arglist = []
        
    for carg, (name, cast, help) in zip(cargs, pargs):
        try:
            arglist.append(casts[cast](carg))
        except ValueError:
            parser.print_help()
            sys.exit('\nERROR: invalid type for "%s". "%s" is not %s' \
                     % (name, carg, cast))

    # move opts to dictionary kws 

    kws = {}
    
    optdests = [o.dest
                for o in parser._short_opt.values()+parser._long_opt.values()
                if o.dest]

    for d in optdests:
        val = getattr(opts,d)
        if val != None:
            kws[d.replace("-","_")] = val

    return func(*arglist, **kws)

if __name__ == "__main__":

    def teller(*args, **kws):
        print "args =", args
        print "kws  =", kws
        
    che(teller, file(sys.argv.pop(1)).read())
