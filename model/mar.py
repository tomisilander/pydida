#!/usr/bin/python

import tempfile

vdfn, datfn, hstfn = n_args_or_bust(3,"vdf datf hstf")

def try_to_predict_missing(varn, i):

    # CREATE DATA 
    dfn  = tempfile.mktemp(".idt")
    datf = open(datfn); df = open(dfn, "w")
    for l in datf.xreadlines():
        t = l.split()
        t[i] = t[i]==-1 and "0" or "1"
        print >>df, "\t".join(t)
    datf.close(); df.close()

    # CREATE VD
    vfn  = tempfile.mktemp(".vd")
    vdf = open(vdfn); vf = open(vfn, "w")
    vdls = vdf.readlines()
    vdf.close()
    vdls[i] = "%s\t0\t1\n" % varn
    map(vf.write,vdls)
    vf.close()
    
    # RUN NB FOR A WHILE
    os.system("%s %s %s %d %d %d %s %s %d /dev/null" \
              % (nblearner, vfn, dfn, dc, i, 1, rfn, sfn, st))

    # READ LOO
    rf = open(rfn)
    loo = float(rf.readline().split()[4])
    rf.close()

    return 100*loo


mcs = table_by_cols(hstfn,2,"\t")[0]
dc = rowc(datfn)
varns = table_by_cols(vdfn,2,"\t")[0]
for varn,i in zip(varns,range(len(varns))):
    mp = 100.0*mcs[i]/dc
    if mp < too_small_percent:
        print "%s\t0\t%.2f" % (varn,mp)
    else :
        loo = try_to_predict_missing(varn, i)
        print "%s\t0\t%.2f\t%.2f" % (varn,mp,loo)
