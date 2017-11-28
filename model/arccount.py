#!/usr/bin/python

from bwutil import *
from operator import __add__

strfn, = n_args_or_bust(1,"strfile")
childcounts = map(int, col(strfn,0))
print reduce(__add__,childcounts)
