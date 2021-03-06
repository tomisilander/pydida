import sys, os, shutil
from itertools import izip, imap

from transpose_file  import transpose

DBG_KEEP = 0; # keep files

def fout(line, missmark, Alpha):
    return ((n != "-1") and (Alpha and "k"+ n.rjust(3,"0") or n) or missmark
            for n in line[:-1].split("\t"))

def lout(line, missmark, Alpha):
    return "\t".join(fout(line, missmark, Alpha))

def colpaste(vns, infn, outfn):
    fout = file(outfn, "w")
    for vn_l in izip(vns, file(infn)):
        fout.write("\t".join(vn_l))

def rowcat(vns, infn, outfn):
    fout = file(outfn, "w")
    print >>fout, "\t".join(vns)
    for l in file(infn):
        fout.write(l)
        
def dout(vdfile, datafile, resdir,
         Alpha=False, Delim="\t", Rowise=False, Names="1", EOL_type="UNIX",
         commands = None, cmd_file = None,
         Missmark = "-1",
         **cmdsyntax):

    dad  = lambda x: os.path.join(resdir, x)
    dtns = lambda phase: dad(os.path.basename(datafile))+"_"+phase
    def clean(fn):
        if not DBG_KEEP: os.remove(fn)

    # INOUT

    # copy code from din


    # ALPHA + MISSMARK

    if (not Alpha) and (Missmark == "-1"):
        shutil.copyfile(datafile, dtns("abc"))
    else:
        adf = file(dtns("abc"), "w")
        for l in file(datafile):
            print >> adf, lout(l, Missmark, Alpha)
        adf.close()
        
    # TRANSPOSE

    if Rowise:
        shutil.copyfile(dtns("abc"), dtns("roc"))
    else:
        transpose(dtns("abc"), dtns("roc"), "\t")

    clean(dtns("abc"))

    # VARS

    vns = [l.split("\t")[0] for l in file(vdfile)]
    
    if Names == "COL":
        colpaste(vns, dtns("roc"), dtns("vdt"))
    elif Names == "ROW":
        rowcat(vns, dtns("roc"), dtns("vdt"))
    else:
        shutil.copyfile(dtns("roc"), dtns("vdt"))

    clean(dtns("roc"))

    # DELIM + EOF

    if Delim and len(Delim)==3 and Delim.isdigit():
        Delim = chr(int(Delim,8))

    if Delim == "\t" and EOL_type == 'UNIX':
        shutil.copyfile(dtns("vdt"), dtns("dat"))
    else:
        outf = file(dtns("dat"),"w")
        em = {'MAC' : "\r", 'WIN' : "\r\n", "UNIX" : "\n"}[EOL_type]
        for l in file(dtns("vdt")):
            outf.write(Delim.join(l[:-1].split()) + em)
        outf.close()

    clean(dtns("vdt"))

    # DAT

    shutil.copyfile(dtns("dat"), dad("dat"))
    clean(dtns("dat"))

    

strusage = """
-D --Delim Delim   : field separator (default tabulator)
-R --Rowise (bool) : one variable per row
-A --Alpha  (bool) : 
-E --EOL EOL-type MAC|UNIX|WIN : default UNIX
-N --Names Names ROW|COL|NONE  : default NONE
-M --Miss Missmark : default "-1"
"""

if __name__ == "__main__":
    import varset, varcmd
    from coliche import che
    dout_strusage = ("""vdfile; datafile; result_dir;"""
                     + strusage
                     + varset.strusage + varcmd.strusage)

    che(dout, dout_strusage)
    resdir = che(lambda *ps, **ks: ps[2], dout_strusage)
    print >>file(os.path.join(resdir, "dout.cmd"), "w"), " ".join(sys.argv)
