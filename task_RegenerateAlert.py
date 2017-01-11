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

def write_next_task(col_name,timestamp):
    query = """
    insert into senslopedb.to_run_scripts(script_name,stat) values ('task_RegenerateAlert.py %s %s','WAITING')
    """ %(col_name,str(timestamp))
#    print query
    db,cur = qdb.SenslopeDBConnect('senslopedb')
    cur.execute(query)
    db.commit()

    return 1   
    
    
def main():  
    name = sys.argv[1]
    date = str(sys.argv[2])
    time = str(sys.argv[3])
    custom_end = pd.to_datetime(date + ' ' + time)
    name = str(name)
    try:
        ad.main(name,custom_end)
        next_timestamp = custom_end + tda(minutes=30)
        if next_timestamp < dt.now():
            print 'will write next task now'
            write_next_task(name,next_timestamp)
            return 1
        else:
            print "++++++++++++++Stopping +++++++++++++++++++"
            return 2
    except:
        return -1




if __name__ == "__main__":
    main()

    
    