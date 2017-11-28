import sys, os, shutil

from formatcheck     import formatcheck
from table2tab_le    import table2tab_le
from vargen          import vargen
from varcheck        import varcheck
from split2var_n_dat import split2var_n_dat
from transpose_file  import transpose
from varsel          import varsel
from misrep          import misrep
from mismark         import mismark
from datyp           import datyp
from datana          import datana

import vars, varcmd

DBG_KEEP = 0; # keep files

def din(datafile, resdir,
        delim=None, rowise=False, names="ROW", start=0,
        keep_empty=False, tabstring=None,
        commands = '', cmd_file = None,
        missmark = "", 
        **cmdsyntax):

    # ENSURE RESDIR

    if not os.path.exists(resdir) or not os.path.isdir(resdir):
        os.makedirs(resdir)

    # HELPERS
    
    dad  = lambda x: os.path.join(resdir, x)
    dtns = lambda phase: dad(os.path.basename(datafile))+"_"+phase
    
    def clean(fn):
        if not DBG_KEEP: os.remove(fn)

    # START BY
    
    shutil.copyfile(datafile, dtns("org"))

    if delim and len(delim)==3 and delim.isdigit():        
        delim = chr(int(delim,8))

    # CHECK IT
    
    (ok, nof_rows, nof_cols, msg) = formatcheck(dtns("org"), delim, keep_empty)

    if not ok:
        return (0, nof_rows, nof_cols, msg)

    # TABIFY
    
    table2tab_le(dtns("org"), dtns("tab"), delim, keep_empty, tabstring)
    clean(dtns("org"))
          
    # VARS

    vnfn = dad("vns.org")
    if names == "GEN":
        vargen(rowise and nof_rows or nof_cols, vnfn, start)
        shutil.copyfile(dtns("tab"),dtns("nov"))
    elif names in ("ROW", "COL"):
        split2var_n_dat(dtns("tab"), vnfn, dtns("nov"), names)
    else:
        shutil.copyfile(names, vnfn)
        shutil.copyfile(dtns("tab"),dtns("nov"))
        
    ok, msg = varcheck(vnfn, rowise and nof_rows or nof_cols)
    if not ok:
        return (0, nof_rows, nof_cols, msg)

    clean(dtns("tab"))

    # VAR/ROW

    if rowise:
        N = nof_cols
        shutil.copyfile(dtns("nov"), dtns("org"))
    else:
        transpose(dtns("nov"), dtns("col"), "\t")
        N = nof_rows
        
    clean(dtns("nov"))

    # SEL

    sx = varcmd.syntax(cmdsyntax)
    new_vnfn = dad("vns")
    varsel(vnfn, dtns("col"), new_vnfn, dtns("sel"),
           commands, cmd_file, **sx)
    vnfn = new_vnfn
    nof_vars = len(vars.vars(vnfn))
    clean(dtns("col"))
    
    # MIS
    
    msfn = dad("mis")

    misrep(vnfn, dtns("sel"), msfn,
           commands, cmd_file, missmark, **sx)

    mismark(vnfn, dtns("sel"), dtns("mis"),
            commands, cmd_file, missmark, **sx)

    clean(dtns("sel"))

    # TYP
    
    tpfn = dad("typ")
    datyp(dtns("mis"), tpfn)

    # ANA -- should this be here or not

    anfn = dad("ana")
    datana(vnfn, dtns("mis"), tpfn, anfn, commands, cmd_file, **sx)

    # DNA

    shutil.copyfile(dtns("mis"),dad("dna"))
    clean(dtns("mis"))



    return (1, N, nof_vars, msg)

strusage = """
-d --delim delim   : field separator (default whitespaces)
-r --rowise (bool) : already one variable per row
-t --tab tabstring : convert tabs to (default:) 8 spaces
-k --keep-empty    : consider lines with whitespace only as proper
-n --names names   : "GEN", "ROW", "COL" or filename,  default "ROW"
-s --start start (int) : if -n GEN : default 0 -> V0, V1, ..
-m --miss missmark : same as -c " .. :: miss miss-mark" : default ""
"""

if __name__ == "__main__":
    import varset, varcmd
    from coliche import che
    
    din_strusage = ("""
    datafile; result_dir;"""
    + strusage
    + """
    -f --cmd-file cmd-file : read commands from file first
    -c --cmd commands      : separated by %s
    """+ varset.strusage + varcmd.strusage)

    r = che(din, din_strusage)

    resdir = che(lambda *ps, **ks: ps[1], din_strusage)
    print >>file(os.path.join(resdir, "din.cmd"), "w"), " ".join(sys.argv)
        
    ok = r[0]

    if ok:
        print 1
        print r[1], r[2]
    else:
        print 0
        print r[3]
