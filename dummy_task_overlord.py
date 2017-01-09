# -*- coding: utf-8 -*-
"""
Created on Mon Jan 09 08:49:56 2017
This scripts gets tasks on queue from the table 'to_run_scripts'.
@author: chocolate server
"""

import MySQLdb as mysqlDriver
import os
#import time

Hostdb = '127.0.0.1'
Userdb = 'root'
Passdb = 'senslope'
nameDB = 'senslopedb'
db = mysqlDriver.connect(host = Hostdb, user = Userdb, passwd = Passdb, db=nameDB)
cur = db.cursor()

def get_waiting_task():
    query = """
    select script_name,script_add from senslopedb.to_run_scripts where stat = 'WAITING' limit 1
    """    
    cur.execute(query)
    entry = cur.fetchall()
    script = entry[0][0]
    address = entry[0][1].replace('\\\\', '\\' )
    address =address.replace('chocolate server', '\\"chocolate server"') #because the path has a space </3
    return script,address
    
#time_now = time.strftime("%Y-%m-%d %H:%M:%S")
#print get_waiting_task()
def mark_task_as_running():
    query = """
    select script_name,script_add from senslopedb.to_run_scripts where stat = 'WAITING' limit 1
    """    

def execute(script,address):
    cmd = '''python %s %s''' %(address,script)    
#    print cmd
    os.system(cmd)
    return 1

execute(get_waiting_task()[0],get_waiting_task()[1])