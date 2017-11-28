def split2var_n_dat(infile, vnsfile, datfile, names="ROW"):
    fin  = file(infile)
    vnsf = file(vnsfile, "w")
    datf = file(datfile, "w")

    if names == "COL":
        for l in fin:
            n, dl = l.split("\t",1)
            print >>vnsf, n
            datf.write(l)
    else:
        vnsf.write(fin.readline().replace("\t","\n"))
        for l in fin:
            datf.write(l)
            
if __name__ == "__main__":
    from coliche import che
    che(split2var_n_dat,
        """
        infile  : variables in a first row separated by TABs
        vnfile  : the file will contain one variable name per row
        datfile : cat infile | tail +2 > datfile
        -n --names names (ROW|COL) : default ROW i.e. variable in the first ROW
        """)
