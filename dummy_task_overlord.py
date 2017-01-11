# -*- coding: utf-8 -*-
"""
Created on Mon Jan 09 08:49:56 2017
This scripts gets tasks on queue from the table 'to_run_scripts'.
@author: chocolate server
"""

import MySQLdb as mysqlDriver
import os
import time
#import sys

Hostdb = '127.0.0.1'
Userdb = 'root'
Passdb = 'senslope'
nameDB = 'senslopedb'
db = mysqlDriver.connect(host = Hostdb, user = Userdb, passwd = Passdb, db=nameDB)
cur = db.cursor()

def get_waiting_task():
    query = """
    select script_name,task_id from senslopedb.to_run_scripts where stat = 'WAITING' limit 1
    """    
    cur.execute(query)
    entry = cur.fetchall()
    if len(entry) > 0:
        script = entry[0][0]
        task_id = int(entry[0][1])
        update_stat_running(task_id)
        return script,address,task_id
    else:
        print 'No more tasks to do. Quit na.'
        return 0

def re_run_task(task_id):
    query = """
    select script_name,task_id from senslopedb.to_run_scripts where task_id = %d limit 1
    """ % int(task_id)
    cur.execute(query)
    entry = cur.fetchall()
    script = entry[0][0]
    task_id = int(entry[0][1])
    update_stat_running(task_id)
    return script,address,task_id
    
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

def update_stat_error(task_id,desc):
    time_now = time.strftime("%Y-%m-%d %H:%M:%S")
    desc = '-' + str(desc)
    query = """
    update senslopedb.to_run_scripts set stat = 'ERROR%s', time_finished = '%s' where task_id = %d
    """ %(desc,str(time_now),task_id)
    cur.execute(query)
    db.commit()
    return 1
    

def execute(script,address,task_id):
    cmd = '''python %s %s''' %(address,script)    
    try:
        if os.system(cmd) == 0:
            update_stat_finished(task_id)
            return 1
        else:
            update_stat_error(task_id,'cmd')
            return task_id
    except:
        update_stat_error(task_id,'update_stat_error')
        return task_id

def main():
    while 1:
        script,address,task_id = get_waiting_task()
        run = execute(script,address,task_id)
        if run != 1:
            script,address,task_id = re_run_task()
            run = execute(script,address,task_id)

if __name__ == '__main__':

