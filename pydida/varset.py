class InvalidVarsetExpression(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def ix(var, varnames, first = True):
    if var.isdigit():  n = int(var)
    elif var:          n = varnames.index(var)
    elif first:        n = 0
    else :             n = len(varnames)-1

    vn = varnames[n] # to raise the exception
    return n

sep_mark = "|"
rng_mark = ".."

def syntax(args):
    return {'sep_mark' : args.get('sep_mark', sep_mark),
            'rng_mark' : args.get('rng_mark', rng_mark)}

def all(varnames):
    return set(xrange(len(varnames)))
               
def varset(vs_expr, varnames, **varsyntax):
    sx = syntax(varsyntax)
    
    try:
        vs = set()
        rngs = map(str.strip, vs_expr.split(sx['sep_mark']))
        for rng in rngs:
            if rng.isdigit() or rng in varnames:
                vs.add(ix(rng, varnames))
            elif rng_mark in rng:
                a,b = map(str.strip, rng.split(sx['rng_mark']))
                a   = ix(a, varnames)
                b   = ix(b, varnames, False)
                vs.update(xrange(a, b + 1, 1))
            else:
                raise InvalidVarsetExpression(vs_expr)
        return vs
    except ValueError:
        raise
    except IndexError:
        raise
    except :
        raise InvalidVarsetExpression(vs_expr)
    
strusage = """
        --sep   sep-mark    : separator token : default "%s"
        --range rng-mark    : range token : default "%s"
""" %(sep_mark, rng_mark)
        
if __name__ == "__main__":

    from coliche import che

    def main(vs_expr, vnfile, sep_mark=sep_mark, rng_mark=rng_mark):
        vs = varset(vs_expr, map(str.strip, file(vnfile)))
        print vs
            
    che(main,
        """
        test-expression : in quotes
        vnfile          : one variable name per row  
        """ + strusage)
