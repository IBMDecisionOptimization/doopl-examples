# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2018
# --------------------------------------------------------------------------

"""
This example show how to run an OPL model with its dat files and run it with the runSeed diagnosis
"""
from doopl.factory import *

import os
from os.path import dirname, abspath, join

DATADIR = join(dirname(abspath(__file__)), 'data')

mod = join(DATADIR, "lifegameip.mod")

with create_opl_model(model=mod) as opl:
    opl.run_seed(5)

