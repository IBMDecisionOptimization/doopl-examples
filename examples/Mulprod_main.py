# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2018
# --------------------------------------------------------------------------

"""
Shows how to do optimization workflows by running several models.
"""
from doopl.factory import *

import os
from os.path import dirname, abspath, join

DATADIR = join(dirname(abspath(__file__)), 'data')
mod = join(DATADIR, "mulprod.mod")
dat = join(DATADIR, "mulprod.dat")

status = 127
capFlour = 20
best = .0
curr = float("inf")


Capacity = pd.DataFrame({'name' : ['flour', 'eggs'], 'value' : [20, 40]})


while (best != curr):
    best = curr
    with create_opl_model(model=mod, data=dat) as opl:
        opl.set_input("Capacity", Capacity)
        print("Solve with capFlour = " + str(capFlour))
        if opl.run():
            curr = opl.objective_value
            print("OBJECTIVE: " + str(curr))
        else:
            print("No solution!")
        capFlour += 1
        Capacity.update(pd.DataFrame({'value' : [capFlour]}))