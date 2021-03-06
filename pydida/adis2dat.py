import array

def dat(vd, ana, dsp, tfields):
    nvals, nfreqs = map(list, ana['nvals'] and zip(*ana['nvals']) or ([],[]))
    avals, afreqs = map(list, ana['avals'] and zip(*ana['avals']) or ([],[]))
    binc, divs = dsp["binc"], dsp["divs"]
    nof_divs   = divs and len(divs) or 0

    nfields = array.array('b',[0]*(ana['numc'] + ana['ascc'] + ana['misc']))
    for j,tfield in enumerate(tfields):
        vix = 0
        if tfield == None:
            vix = -1
        elif isinstance(tfield,str) :
            vix = binc + avals.index(tfield)
        else : # find bin
            if nof_divs:
                v = float(tfield)
                if v > divs[-1]:
                    vix = nof_divs
                else:
                    for (divix, d) in enumerate(divs):
                        if d >= v:
                            vix = divix
                            break;
            else:
                vix = nvals.index(tfield)

        nfields[j] = vix

    return nfields


def hst(nfields, vd):
    
    valsfrq = [0] * (len(vd["vds"]) + 1)

    for n in nfields:
        valsfrq[n] += 1

    return valsfrq
