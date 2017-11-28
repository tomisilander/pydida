#!/usr/bin/python

from itertools import chain, imap, repeat
import re, coliche

def ffiter(f, sz, sep):
    global eof
    re_sep = re.compile(sep)
    
    def fliter():

        def linesegs():
            global eof
            eoln = False
            while not eoln:
                l = f.readline(sz)

                if not l :
                    eof = True
                    break
        
                if l[-1] == "\n":
                    eoln = True
                    yield l[:-1]
                else:
                    c = ""
                    x = ""
                    while c != "\n" and not re_sep.match(c):
                        x += c
                        c = f.read(1)
                        if not c: break
                    eoln = c and c == "\n" 
                    yield l + x

        lsegiters = imap(re_sep.split, linesegs())
        
        for field in chain(*lsegiters):
            yield field

    eof = False
    while not eof:
        yield fliter()



def main(filename, size=1024, sep="\t"):
    for lno, lfer in enumerate(ffiter(file(filename), size, sep)):
        for fno, f in enumerate(lfer):
            print lno, fno, f



if __name__ == "__main__":
    coliche.che(main,
                """ filename
                -s --size size (int) : chunk size in bytes (default 1024)
                -d --sep sep : separator (default "\t")""")
