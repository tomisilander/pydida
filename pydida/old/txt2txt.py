from bwutil import linen2list
from itertools import izip
from transpose_file import transpose_file
import tempfile

def main(txtfile, anafile, ana2file, txt2file,
         transposed=False, sep=None):

    if transposed :
        ttxtfn  = txtfile
        ttxt2fn = txt2file
    else:
        ttxtfn = tempfile.mktemp()
        transpose_file(txtfile, ttxtfn);
        ttxt2fn = tempfile.mktemp()


    ttxt2f  = file(ttx2fn, "w")
    osep    = sep and sep or " "
    
    for al,a2l,dl in izip(file(anafile), file(ana2file), file(txtfile)):
        avs    = linen2list(al, "\t")[6:]
        a2vs   = linen2list(a2l,"\t")[6:]
        trans  = dict(izip(avs,a2vs))
        vn,ds  = linen2list(dl,sep,None,1)
        print >> ttxt2f, vn+osep
        print >> ttxt2f, osep.join([trans.get(d,d) for d in ds])
    
    ttxt2f.close()

    
    if not transposed :
        transpose_file(ttxtfn, txt2file);
        os.unlink(ttxtfn)
        os.unlink(ttxt2fn)
    

if __name__ == "__main__":
    from coliche import che
    che(main, """"txtfile; anafile; ana2file; txt2file
        -t --transposed (bool) : input and output transposed
        -s --sep sep : separator : default whitespace
        """)
