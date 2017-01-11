# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 08:25:40 2017

@author: chocolate server
"""

import pandas as pd
import querySenslopeDb as qdb

#
def get_cols():
    query = "select name from senslopedb.site_column_props "
    query2 = """where name like '____%' """
    query = query + query2
    return qdb.GetDBDataFrame(query)

def write_initial_task(col_name):
    timestamp = pd.to_datetime('2016-10-01 00:00:00')
    query = """
    insert into senslopedb.to_run_scripts(script_name,stat) values ('task_RegenerateAlert.py %s %s','WAITING')
    """ %(col_name,str(timestamp))
    db,cur = qdb.SenslopeDBConnect('senslopedb')
    cur.execute(query)
    db.commit()
#    db.close()
    return 1
    
cols  = get_cols()
for i in range(0,len(cols)):
    write_initial_task(cols.iloc[i][0])