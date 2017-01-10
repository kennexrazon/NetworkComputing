# -*- coding: utf-8 -*-
"""
Created on Mon Jan 09 08:49:56 2017
This scripts gets tasks on queue from the table 'to_run_scripts'.
@author: chocolate server
"""

import MySQLdb as mysqlDriver
import os
import time
import sys

Hostdb = '127.0.0.1'
Userdb = 'root'
Passdb = 'senslope'
nameDB = 'senslopedb'
db = mysqlDriver.connect(host = Hostdb, user = Userdb, passwd = Passdb, db=nameDB)
cur = db.cursor()

def get_waiting_task():
    query = """
    select script_name,script_add,task_id from senslopedb.to_run_scripts where stat = 'WAITING' limit 1
    """    
    cur.execute(query)
    entry = cur.fetchall()
    if len(entry) > 0:
        script = entry[0][0]
        address = entry[0][1]
#        address = entry[0][1].replace('\\\\', '\\' )
#        address =address.replace('chocolate server', '\\"chocolate server"') #because the path has a space </3
        task_id = int(entry[0][2])
        update_stat_running(task_id)
        return script,address,task_id
    else:
        print 'No more tasks to do. Quit na.'
        time.sleep(5)
        os.system('''python dummy_task_overlord.py''')

    
def update_stat_running(task_id):
    name = os.environ['COMPUTERNAME']
    time_now = time.strftime("%Y-%m-%d %H:%M:%S")
    query = """
    update senslopedb.to_run_scripts set stat = 'RUNNING', worker = '%s', time_start = '%s' where task_id = %d
    """ %(name,str(time_now),task_id)
    cur.execute(query)
    db.commit()
    return 1
    
def update_stat_finished(task_id):
    time_now = time.strftime("%Y-%m-%d %H:%M:%S")
    query = """
    update senslopedb.to_run_scripts set stat = 'FINISHED', time_finished = '%s' where task_id = %d
    """ %(str(time_now),task_id)
    cur.execute(query)
    db.commit()
    return 1

def update_stat_error(task_id):
    time_now = time.strftime("%Y-%m-%d %H:%M:%S")
    query = """
    update senslopedb.to_run_scripts set stat = 'ERROR', time_finished = '%s' where task_id = %d
    """ %(str(time_now),task_id)
    cur.execute(query)
    db.commit()
    return 1
    

def execute(script,address,task_id):
    cmd = '''python %s %s''' %(address,script)    
    try:
        os.system(cmd)
        update_stat_finished(task_id)
        os.system('''python dummy_task_overlord.py''')
    except:
        os.system(cmd)
        update_stat_error(task_id)
    return 1
    
script,address,task_id = get_waiting_task()
execute(script,address,task_id)