# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2018
# --------------------------------------------------------------------------

"""
This example shows how to convert the integer variables to floating point variables and back to the previous state.
"""
from doopl.factory import *

import os
from os.path import dirname, abspath, join

DATADIR = join(dirname(abspath(__file__)), 'data')
mod = join(DATADIR, 'convert.mod')

# Create the OplModel
with create_opl_model(model=mod) as opl:
    opl.run()
    # Get the engine objective value
    print('objective=%s' % opl.objective_value)

    # convert all integer variables to float
    opl.convert_all_intvars()
    opl.run()
    print('converted=%s' % opl.objective_value)

    # get back to previous state
    opl.unconvert_all_intvars()
    opl.unmute()
    opl.run()
    print('unconverted=%s' % opl.objective_value)