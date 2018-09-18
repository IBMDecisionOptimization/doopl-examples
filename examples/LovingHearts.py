# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2018
# --------------------------------------------------------------------------

"""
This example shows how to apply a .ops file to an OPL model and will run the OPL profiler
"""
from doopl.factory import *

import os
from os.path import dirname, abspath, join

DATADIR = join(dirname(abspath(__file__)), 'data')
mod = join(DATADIR, "loving_hearts.mod")

with create_opl_model(model=mod) as opl:
    opl.apply_ops_file(join(DATADIR, "loving_hearts.ops"))
    opl.use_profiler()
    opl.run()
    print('objective=%s' % opl.objective_value)
