#!/usr/bin/env python
from bwutil import *

def defcmd(ana, nomlimit, cmd, cmdarg):
    if ana["numvc"] < 3 or (ana["numvc"] + ana["ascvc"]) < nomlimit :
        return {"cmd":"NOM"}
    else :
        return {"cmd":cmd,
                "arg":min(ana["numvc"], cmdarg)}

    
def main(anafn, nomlimit, cmd, cmdarg, cmdfn):
    genmain((anafn,),(cmdfn,),defcmd, (nomlimit, cmd, cmdarg))
    
if __name__ == "__main__":
    argscall(main, "anafile nomlimit cmd cmdarg cmdfile",{int:(1,3)})
