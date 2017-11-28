
def analyse(l, usercmds):

    nvals, avals = set(), set()

    for field in usercmds["ADDVALS"]:
        if isinstance(field, str) :
           avals.add(field)
        else :
            nvals.add(field)            

    
    (tfields, numc, ascc) = ([], 0, 0)
    
    for field in l[:-1].split("\t"):
        tfield = field
        for cast in int, float:
            try :
                tfield = cast(field)
                break
            except: pass

        if isinstance(tfield, str) :
            if tfield:
                avals.add(tfield)
                ascc += 1
            else:
               tfield = None
        else:
            nvals.add(tfield)
            numc += 1

        tfields.append(tfield)

    ana = {'numc'  : numc,
           'ascc'  : ascc,
           'nvals' : list(nvals),
           'avals' : list(avals),
           'numvc' : len(nvals),
           'ascvc' : len(avals),
           'min'   : 0,
           'max'   : 0
           }
    
    ana['nvals'].sort()
    ana['avals'].sort()

    if ana['numvc'] > 0 :
        ana['min'] = ana['nvals'][0]
        ana['max'] = ana['nvals'][-1]

    ana['type'] = ana['ascvc'] and ana['numvc'] and 'X' \
                  or ana['ascvc'] and 'A' \
                  or ana['numvc'] and 'N' \
                  or 'M'
    
    return (ana, tfields)
