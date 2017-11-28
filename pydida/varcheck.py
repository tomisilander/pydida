import vars

def varcheck(vnfile, nof_vars=None):

    varnames = vars.vars(vnfile)
    lenvars  = len(varnames)
    dups = len(set(varnames)) < lenvars

    if dups:
        while varnames:
            vn = varnames.pop(0)
            if vn in varnames:
                return (False, "Variable name %s occurs twice." % vn)

    if nof_vars != None and lenvars != nof_vars:
        msg = "Expected %d variable names, but got %d." % (nof_vars, lenvars)
        return (False, msg)
                        
    return (True, "OK")
    
if __name__ == "__main__":
    from coliche import che
    ok, msg = che(varcheck,
                  """vnfile : the file containing varnames one per row""")
    print bool(ok)
    print msg
