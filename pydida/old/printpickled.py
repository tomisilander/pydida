#!/usr/bin/env pythonimport sys, pickle
import coliche

def main(filename):
    f = file(filename)

    while True:
        try:    print pickle.load(f)
        except: break

    f.close()

coliche.che(main, "filename")
