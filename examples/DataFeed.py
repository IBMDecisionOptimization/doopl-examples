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
from os.path import abspath, dirname, join
import sys

import pandas as pd

DATADIR = join(dirname(abspath(__file__)), 'data')
filename = join(DATADIR, 'bigsql.mod')


size = 5


def generate():
    #### This method is creating artefacts for the sample. Not really interesting method, may have ugly code.
    if not os.path.isdir(DATADIR):
        os.makedirs(DATADIR)
    num_lines = 0
    try:
        num_lines = sum(1 for line in open(join(DATADIR, 'bigsql.csv'))) -1
    except:
        pass
    if num_lines != size * size * size:
        print("Generating .db file, .dat file and .csv file is starting!")
        try:
            os.remove(join(DATADIR, 'bigsql.db'))
            os.remove(join(DATADIR, 'bigsql.dat'))
            os.remove(join(DATADIR, 'bigsql.csv'))
        except OSError:
            pass
        import sqlite3
        conn = sqlite3.connect(join(DATADIR, "bigsql.db"))
        cur = conn.cursor()
        cur.execute("create table entities (a,b,c,d,e,f,g,h,i,m,n,o,p,q)")
        for i in range(size):
            for j in range(size):
                word = "word"+str(i)+str(j)
                line = [(i,j,k, i,j,k, i,j,k, word+str(k), word+str(k), word+str(k), word+str(k), word+str(k)) for k in range(size)]
                cur.executemany("insert into entities values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", line)
                conn.commit()
        conn.close()

        import sqlite3
        with sqlite3.connect(join(DATADIR,"bigsql.db")) as conn:
                #create the OplModel with 1 .mod
            with create_opl_model(model=filename) as opl:
                opl.mute()
                # pump a table from the DB.
                opl.set_input("entities", pd.read_sql_query("select * from entities", conn))
                opl.setExportExternalData(join(DATADIR, "bigsql.dat"))
                #generate, solve and post process
                opl.run()
                opl.get_table("entities").to_csv(join(DATADIR, "bigsql.csv"), index=False)
                print("Generating .db file, .dat file and .csv file is done!")


def run(task):
    print("Starting task: "+task)
    csvfile = None
    conn = None
    cur = None
    with create_opl_model(model=filename) as opl:
        opl.mute()
        if task == "SQLITE":
            # pump a table from the DB.
            import sqlite3
            conn = sqlite3.connect(join(DATADIR, "bigsql.db"))
            opl.set_input("entities", pd.read_sql_query("select * from entities", conn))
        elif task == "CURSOR":
            import sqlite3
            conn = sqlite3.connect(join(DATADIR, "bigsql.db"))
            cur = conn.cursor()
            cur.execute('select * from entities')
            opl.set_input("entities", cur)
        elif task == "DATFILE":
            opl.set_input(join(DATADIR, "bigsql.dat"))
        elif task == "PANDAS":
            opl.set_input("entities", pd.read_csv(join(DATADIR, "bigsql.csv")))
        elif task == "CSV":
            import csv
            if sys.version_info[0] > 2:
                csvfile = open(join(DATADIR, "bigsql.csv"), "rt", encoding="utf-8")
            else:
                # python 2 has no encoding param. Use codecs.open, but
                # there's no "t" mode either
                import codecs
                csvfile = codecs.open(join(DATADIR, "bigsql.csv"), "r", encoding="utf-8")
            reader = csv.reader(csvfile)
            # skip headers
            next(reader)
            opl.set_input("entities", reader)
        opl.run()
        if csvfile is not None:
            csvfile.close()
        if conn is not None:
            if cur is not None:
                cur.close()
            conn.close()
generate()

tasks = ["PANDAS","CSV","SQLITE","CURSOR","DATFILE"]
for t in tasks:
    run(t)
