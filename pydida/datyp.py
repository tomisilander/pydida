import sys
from itertools import imap

def typify(field):
    for t, cast in zip("IF", (int, float)):
        try :
            return t, cast(field)
        except:
            pass
    return (field and "S" or "M"), field 
    

def datyp(datfile, typfile):

    typf = typfile == "-" and sys.stdout or file(typfile,"w")

    for l in file(datfile):
        fields = l[:-1].split("\t")
        ts = (t for (t,f) in imap(typify, fields))
        print >>typf, "".join(ts)

if __name__ == "__main__":
    from coliche import che
    che(datyp,
        """
        datfile  : the file containing one variable per row
        typfile  : file for types of data entries (Int, Float, String, Miss)
        """)
