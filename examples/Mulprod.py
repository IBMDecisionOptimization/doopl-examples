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
mod = join(DATADIR, "mulprod.mod")
dat = join(DATADIR, "mulprod.dat")
dat2 = join(DATADIR, "mulprod2.dat")
gen_dir = os.path.join(DATADIR, "generated")

if not os.path.isdir(gen_dir):
    os.makedirs(gen_dir)


with create_opl_model(model=mod, data=[dat, dat2]) as opl:
    opl.run()

    print(opl)
    print(opl.objective_value)
    print(opl.get_table("OutsideSolution"))
    print(opl.get_table("InvSolution"))
    print(opl.report)

    print('Generating csv in %s' % os.path.join(gen_dir, "capacity.csv"))
    opl.get_table("Capacity").to_csv(os.path.join(gen_dir, "capacity.csv"), index=False)

