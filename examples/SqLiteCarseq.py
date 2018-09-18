# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2018
# --------------------------------------------------------------------------

"""
This example shows how to run an OPL Model by feeding it with tuple lists, and some pandas dataframe from a SQL connection.
"""
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


# create a connection to a DB to use it with pandas.
import sqlite3
conn = sqlite3.connect(join(DATADIR, "carseq.db"))
# create the factory
with create_opl_model(model=filename) as opl:
    # add input tables as IloTupleSet. Can be tuples or pandas df.
    opl.set_input("nbCars", nbCars)
    opl.set_input("nbOptions", nbOptions)
    opl.set_input("nbSlots", nbSlots)
    opl.set_input("demand", demand)
    opl.set_input("capacity", capacity)

    # pump a table from the DB.
    opl.set_input("option", conn.execute('select * from option').fetchall())
    # It could also come from pandas sql reader
    # opl.set_input("option", pd.read_sql_query("select * from option", conn))

    # generate, solve and post process
    opl.run()

    # Get the names of post processing tables
    print("Table names are: "+ str(opl.output_table_names))
    # Get all the post processing tables as dataframes.
    for name, table in iteritems(opl.report):
        print("Table : " + name)
        for t in table.itertuples(index=False):
            print(t)
conn.close()

"""
To use database, one might look at pyodbc library for example.
Here are 2 interesting links:
https://gist.github.com/hunterowens/08ebbb678255f33bba94
https://blogs.msdn.microsoft.com/cdndevs/2015/03/11/python-and-data-sql-server-as-a-data-source-for-python-applications/
"""