# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2018
# --------------------------------------------------------------------------

"""
This example show how to run an OPL model with its dat files, then query the post processing IloTupleSets.
It also shows how to generate CSV files to be used with DO4DSX, the optimization addon to IBM DSXL
"""
from doopl.factory import *

import os
from os.path import dirname, abspath, join

DATADIR = join(dirname(abspath(__file__)), 'data')

mod = join(DATADIR, "nurses.mod")
dat = join(DATADIR, "nurses.dat")

with create_opl_model(model=mod, data=dat) as opl:
    opl.print_conflict()
    print("=====================")
    print(opl.print_relaxation())

