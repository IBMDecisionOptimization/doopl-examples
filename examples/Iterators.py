# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2018
# --------------------------------------------------------------------------

"""
This example shows how to run an OPL model, get a post processing IloTupleSet as a pandas df and iterate on it.
"""
from doopl.factory import *
import os
from os.path import dirname, abspath, join

DATADIR = join(dirname(abspath(__file__)), 'data')

mod = join(DATADIR, "iterators.mod")

with create_opl_model(model=mod) as opl:
    opl.run()

    list = opl.get_table("solution")
    for t in list.itertuples(index=False):
        print(t)
