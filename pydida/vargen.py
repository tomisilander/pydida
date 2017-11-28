import sys

def vargen(nof_vars, outfile, start=0):

    varnames = ["V%d" % (n+start) for n in xrange(nof_vars)]

    fout = (outfile == "-") and sys.stdout or file(outfile, "w")
    print >>fout, "\n".join(varnames)
    
if __name__ == "__main__":
    from coliche import che
    che(vargen,
        """nof_vars (int); outfile
        -s --start start (int) : default 0 -> V0, V1, ..
        """)
