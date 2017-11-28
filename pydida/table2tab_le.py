
# Convert file to the tab limited format

def tabify(fin, delim, fout, keep_empty=False, tabstring=None):

    for line in fin:

        if (not keep_empty) and (not line.strip()) :
            continue

        if tabstring != None:
            line = line.replace("\t", tabstring)

        print >>fout, "\t".join(line[:-1].split(delim))


def table2tab_le(infn, outfn, delim=None, keep_empty=False, tabstring=None):

    if delim == '\\t': delim = '\t' # HMM - maybe "TAB"

    fout = (outfn == "-") and sys.stdout or file(outfn, "w")
    tabify(file(infn, "rU"), delim, fout, keep_empty, tabstring)

if __name__ == "__main__":
    import coliche
    coliche.che(table2tab_le.py,
                """datafile; outfile
                -d --delim delim : field separator (default whitespaces)
                -t --tab tabstring : convert tabs to (default:) 8 spaces
                -k --keep-empty : consider lines with whitespace only as proper
                """)
