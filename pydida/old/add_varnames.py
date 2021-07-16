#!/usr/bin/env python
# infile in unix format - not transposed

def main(infile, outfile, sep=None):
    colcount = len(file(infile).readline()[:-1].split(sep))
    headerline = sep.join("V%d" % (i+1) for i in xrange(colcount)])+"\n"

    of = file(outfile,"w")
    of.write(headerline)
    for l in file(infile): of.write(l)

if __name__ == "__main__":
    import coliche
    coliche.che(main, "infile; outfile; -d --sep sep : field separator")
