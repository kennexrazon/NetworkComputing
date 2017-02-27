 # -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 15:38:12 2016

@author: chocolate server
"""

import pandas as pd
import querySenslopeDb as qdb
from datetime import timedelta as tda
from datetime import datetime as dt
import alertgenDELAYED2 as ad
import sys
from sqlalchemy import exc

def write_next_task(col_name,timestamp):
    query = """
    insert into senslopedb.to_run_scripts(script_name,stat) values ('task_RegenerateAlert.py %s %s','WAITING')
    """ %(col_name,str(timestamp))
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
    next_timestamp = custom_end + tda(minutes=30)
    try:
        ad.main(name,custom_end)
        if next_timestamp < dt.now():
#            write_next_task(name,next_timestamp)
            return 1 #baka return value may problem???
        else:
            print "++++++++++++++Stopping +++++++++++++++++++"
            return 2
    except exc.IntegrityError:
        print '------------IntegrityError------------'
#        if next_timestamp < dt.now():
#            write_next_task(name,next_timestamp)
        return 1 # okay lang di maoverwrite yung nakasulat na sa db
    else:
        print 'ibang error pa'
        return -1

#logf = open("download.log", "w")
#for download in download_list:
#    try:
#        # code to process download here
#    except Exception as e:     # most generic exception you can catch
#        logf.write("Failed to download {0}: {1}\n".format(str(download), str(e)))
#        # optional: delete local version of failed download
#    finally:
#        # optional clean up code
#        pass



if __name__ == "__main__":
    main()

    
    