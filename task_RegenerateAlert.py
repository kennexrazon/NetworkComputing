 # -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 15:38:12 2016

@author: chocolate server
"""

import pandas as pd
import querySenslopeDb as qdb
from datetime import timedelta as tda
from datetime import datetime as dt
import alertgenDELAYED as ad
import sys

def get_cols():
    query = "select name from senslopedb.site_column_props "
    query2 = """where name like '____%' """
    query = query + query2
    return qdb.GetDBDataFrame(query)

#def write_initial_task(col_name):
#    timestamp = pd.to_datetime('2016-10-01 00:00:00')
#    query = """
#    insert into senslopedb.to_run_scripts(script_name,script_add,stat) values ('task_RegenerateAlert.py %s %s',"",'WAITING')
#    """ %(col_name,str(timestamp))
#    db,cur = qdb.SenslopeDBConnect('senslopedb')
#    cur.execute(query)
#    db.commit()
#    db.close()
#    return 1
#    
#cols  = get_cols()
#for i in range(0,len(cols)):
#    write_initial_task(cols.iloc[i][0])

def write_next_task(col_name,timestamp):
    query = """
    insert into senslopedb.to_run_scripts(script_name,script_add,stat) values ('task_RegenerateAlert.py %s %s',"",'WAITING')
    """ %(col_name,str(timestamp))
    db,cur = qdb.SenslopeDBConnect('senslopedb')
    cur.execute(query)
    db.commit()
    db.close()
    return 1   
    
    
def main():  
    name = sys.argv[1]
    custom_end = pd.to_datetime(sys.argv[2])
    name = str(name)
    ad.main(name,custom_end)
    next_timestamp = custom_end + tda(minutes=30)
    if next_timestamp < dt.now():
        write_next_task(name,next_timestamp)
    else:
        print "================Stopping =================="


if __name__ == "__main__":
    main()

    
    