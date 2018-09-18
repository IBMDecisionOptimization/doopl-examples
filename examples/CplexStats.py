# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2018
# --------------------------------------------------------------------------

"""
This example show how to run an OPL model with its dat files, then query CPLEX statistics
"""
from doopl.factory import *

import os
from os.path import dirname, abspath, join

DATADIR = join(dirname(abspath(__file__)), 'data')
mod = join(DATADIR, 'lifegameip.mod')

with create_opl_model(model=mod) as opl:
    opl.mute()
    opl.run()
    stats = opl.cplex_stats
    quality = opl.cplex_quality
    print(opl)
    for k,v in iteritems(stats):
        if v != 0:
            print("key: "+k+" value: "+str(v))

    for k,v in iteritems(quality):
        v = quality[k]
        if v != 0:
            print("quality: "+k+" value: "+str(v))
