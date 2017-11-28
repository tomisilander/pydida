#!/usr/bin/python

from sets import Set, ImmutableSet

class UnknownUserCommand(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InvalidRangeExpression(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def ix(var, varnames, first = True):
    if var.isdigit():  return int(var)
    elif var:          return varnames.index(var)
    elif first:        return 0
    else :             return len(varnames)-1
    
class UserCommands :
    def __init__(self, varnames, fn=None):
        self.varnames = varnames
        self.varc =len(varnames)
        self.inize()
        if not fn: return
        
        for line in file(fn):
            vars_s, cmd_s = l.split("\t")
            for v in s2intset(vars_s):
                docmd(v, cmd_s)

    def s2intset(self, vars_s):
        try:
            rngs = imap(str.strip, vars_s.split(","))
            for rng in rngs:
                if rng in self.varnames or rng.isdigit():
                    yield ix(rng, self.varnames)
                elif "-" in rng:
                    a,b = map(str.strip, rng.split("-"))
                    a   = ix(a, varnames)
                    b   = ix(b, varnames, False)
                    for v in xrange(ix(a, varnames), ix(b, varnames)+ 1, 1):
                        yield v
                else:
                    raise InvalidRangeExpression(vars_s)
        except:
            raise InvalidRangeExpression(vars_s)
        
    def inize(self):
        self.ins  = [True] * self.varc
        self.diss = [("AFTERLIMIT", (6,"EQW",4))] * self.varc
        self.vals = [set() for v in self.varnames]
        
    def docmd(self, v, cmd_s):
        cmd, args_s = cmd_s.split(None,cmd_s)
        cmd = cmd.upper()
        args = typefy(args_s.split()) #Hmm, should this be postponed
        if cmd == "IN" or cmd == "OUT" :
            self.ins[v] = cmd == "IN"
        elif cmd == "DIS":
            self.diss[v] = (args[0], args[1:])
        elif cmd == "ADDVALS" :
            self.vals[v].union_update(args)
        else :
            raise UnknownUserCommand("VarIndex = %d, Cmd = (%s)" % (v, cmd_s))
                

    def varcmds(self,v):
        return {"IN"      : self.ins[v],
                "ADDVALS" : self.vals[v],
                "DIS"     : self.diss[v]}

#import sys
#p = UserCommands("c",2)
#print [i for i in p.s2intset(" ".join(sys.argv[1:]))]
       
