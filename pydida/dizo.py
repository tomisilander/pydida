#!/usr/bin/python

if __name__ == "__main__":
    import os, sys
    import din, diz, dout, varset, varcmd
    from coliche import che

    def main(datafile, resdir, **optargs):

        dad = lambda x : os.path.join(resdir, x)

        ############### D I N ##############

        
        r = din.din(datafile, resdir, **optargs)

        if not r[0]:
            print 0
            sys.exit(r[3])


        ############### D I Z ##############


        posargs = map(dad, ("vns","dna","ana","typ")) + [resdir]
        diz.diz(*posargs, **optargs)


        ##############D O U T #############


        posargs = (dad("vds"), dad("dzd"), resdir)
        dout.dout(*posargs, **optargs)

        ############# SAVE CMD LINE

    strusage = ("""datafile; result_dir;"""
                + din.strusage
                + diz.strusage
                + dout.strusage
                + """
                -f --cmd-file cmd-file : read commands from file first
                -c --cmd commands : separated by %s
                """+ varset.strusage + varcmd.strusage)
    
    che(main, strusage)
    resdir = che(lambda *ps, **ks: ps[1], strusage)
    print >>file(os.path.join(resdir, "dizo.cmd"), "w"), " ".join(sys.argv)
