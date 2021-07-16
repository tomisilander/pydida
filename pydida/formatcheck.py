#!/usr/bin/env python
# This module checks that the data file conforms to the simple
# tabular format.

def msg(lineno, nof_cols0, nof_cols, fields):
    return """
        The number of values expected on line %d is %d
        (i.e as many as there are fields in the first row),
        but the number of values found was %d
        (or actually number of field separators found was %d).
        Values found are (separated by semicolon):(%s)
        """ % (lineno+1, nof_cols0, nof_cols, nof_cols-1, ";".join(fields))

def formatcheck(infn, delim, keep_empty=False):
    nof_cols0 = 0
    nof_empty = 0
    lineno = -1
    f = file(infn,"rU")

    for lineno, line in enumerate(f):
        
        if (not keep_empty) and (not line.strip()) :
            nof_empty += 1
            continue

        t = line[:-1].split(delim)
        nof_cols = len(t)
        if not nof_cols0: nof_cols0 = nof_cols
        if nof_cols != nof_cols0:
            return False, 0, 0, msg(lineno, nof_cols0, nof_cols, t)
        
    return True, lineno + 1 - nof_empty, nof_cols0, ""

# And if so (and even if not) makes the result tab limited


def main(infn, delim=None, keep_empty=False):

    if delim == '\\t': delim = '\t'
    
    ok, nof_rows, nof_cols, msg = formatcheck(infn,delim, keep_empty)

    print int(ok);
    print ok and ("%d %d" % (nof_rows, nof_cols)) or msg

if __name__ == "__main__":
    from coliche import che
    che(main,
        """datafile
        -d --delim delim : field separator (default whitespaces)
        -k --keep-empty (bool) : don't skip empty lines
        """)
