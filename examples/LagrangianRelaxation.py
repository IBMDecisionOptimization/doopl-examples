# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2018
# --------------------------------------------------------------------------

"""
This example show a Lagrangian relaxation to illustrate multi model workflows
"""
from doopl.factory import *

import os
from os.path import dirname, abspath, join

DATADIR = join(dirname(abspath(__file__)), 'data')
GENDIR = os.path.join(DATADIR, "generated")

mod = join(DATADIR, "lagrange.mod")

Bs = [(0, 15), (1, 15), (2, 15)]
Cs = [(0,0,6), (0,1,10), (0,2,1), (1,0,12), (1,1,12), (1,2,5), (2,0,15), (2,1,4), (2,2,3), (3,0,10), (3,1,3), (3,2,9), (4,0,8), (4,1,9), (4,2,5)]
As = [(0,0,5), (0,1,7), (0,2,2), (1,0,14), (1,1,8), (1,2,7), (2,0,10), (2,1,6), (2,2,12), (3,0,8), (3,1,4), (3,2,15), (4,0,6), (4,1,12), (4,2,5)]

max_iters = 101

print("#As={}, #Bs={}, #Cs={}".format(len(As)//len(Bs), len(Bs), len(Cs)//len(Bs)))

# lagrangian relaxation loop
eps = 1e-6
loop_count = 0
best = 0
initial_multiplier = 1
number_of_cs = len(Cs)//len(Bs)
c_range = range(number_of_cs)

multipliers = [(i,initial_multiplier) for i in c_range]

while loop_count <= max_iters:
    loop_count += 1
    # rebuilt at each loop iteration
    with create_opl_model(model=mod) as opl:
        opl.set_input("A", As)
        opl.set_input("B", Bs)
        opl.set_input("C", Cs)
        opl.set_input("multipliers", multipliers)
        opl.mute()
        opl.export_model(os.path.join(GENDIR, "cplex"+str(loop_count)+".lp"))

        if not opl.run():
            print("*** solve fails, stopping at iteration: %d" % loop_count)
            break
        best = opl.objective_value
        penalties = [t.value for t in opl.get_table("penalties").itertuples(index=False)]
        print('%d> new lagrangian iteration:\n\t obj=%g, m=%s, p=%s' % (loop_count, best, str([t[1] for t in multipliers]), str(penalties)))

        do_stop = True
        justifier = 0
        for k in c_range:
            penalized_violation = penalties[k] * multipliers[k][1]
            if penalized_violation >= eps:
                do_stop = False
                justifier = penalized_violation
                break

        if do_stop:
            print("* Lagrangian relaxation succeeds, best={:g}, penalty={:g}, #iterations={}"
                  .format(best, opl.get_kpi("total_penalty"), loop_count))
            break
        else:
            # update multipliers and start loop again.
            scale_factor = 1.0 / float(loop_count)
            multipliers = [(i, max(multipliers[i][1] - scale_factor * penalties[i], 0.)) for i in c_range]
            print('{0}> -- loop continues, m={1!s}, justifier={2:g}'.format(loop_count, [t[1] for t in multipliers], justifier))

print("Best is {0}".format(best))

