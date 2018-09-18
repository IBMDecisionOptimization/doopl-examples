# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2018
# --------------------------------------------------------------------------

from sqlalchemy import create_engine

from doopl.factory import *

import os
from os.path import dirname, abspath, join

import pandas as pd

DATADIR = join(dirname(abspath(__file__)), 'data')
filename = join(DATADIR, "carseq.mod")

nbCars = pd.DataFrame([(6)])
nbOptions = pd.DataFrame([(5)])
nbSlots =pd.DataFrame([(10)])

demand = pd.DataFrame([(1,1), (2,1), (3,2), (4,2), (5,2), (6,2)])
capacity = [(1,1,2), (2,2,3), (3,1,3), (4,2,5), (5,1,5)]

option = [(1, 1, 1), (1, 2, 0), (1, 3, 0), (1, 4, 0), (1, 5, 1), (1, 6, 1), (2, 1, 0), (2, 2, 0), (2, 3, 1), (2, 4, 1),
          (2, 5, 0), (2, 6, 1), (3, 1, 1), (3, 2, 0), (3, 3, 0), (3, 4, 0), (3, 5, 1), (3, 6, 0), (4, 1, 1), (4, 2, 1),
          (4, 3, 0), (4, 4, 1), (4, 5, 0), (4, 6, 0), (5, 1, 0), (5, 2, 0), (5, 3, 1), (5, 4, 0), (5, 5, 0), (5, 6, 0)]


conn = create_engine('sqlite:///:memory:', echo=True)
#first push the table option into the database
cur = conn.connect()
query = "create table option (a,b,c)"
cur.execute(query)
query = "create table slotSolution (Slots,value)"
cur.execute(query)
query = "create table setupSolution (Options,Slots,value)"
cur.execute(query)
#cur.commit()
cur.execute("insert into option values (?,?,?)", option)
#cur.commit()

# create the factory
with create_opl_model(model=filename) as opl:
    # add input tables as IloTupleSet. Can be tuples or pandas df.
    opl.set_input("nbCars", nbCars)
    opl.set_input("nbOptions", nbOptions)
    opl.set_input("nbSlots", nbSlots)
    opl.set_input("demand", demand)
    opl.set_input("capacity", capacity)

    # pump a table from the DB: pass a sql alchemy cursor.
    opl.set_input("option", cur.execute('select * from option').fetchall())

    # generate, solve and post process
    opl.run()


    # Get the names of post processing tables
    outputs = opl.output_table_names
    print("Table names are: "+ str(outputs))
    for name in outputs:
        opl._to_sql(conn, name)


"""
To use database, one might look at pyodbc library for example.
Here are 2 interesting links:
https://gist.github.com/hunterowens/08ebbb678255f33bba94
https://blogs.msdn.microsoft.com/cdndevs/2015/03/11/python-and-data-sql-server-as-a-data-source-for-python-applications/
"""