# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 16:18:42 2017

@author: chocolate server
"""

import MySQLdb as mysqlDriver
#from datetime import datetime as dt
import time
import sys

def main():
    
    write = sys.argv[1]
    Hostdb = '127.0.0.1'
    Userdb = 'root'
    Passdb = 'senslope'
    nameDB = 'senslopedb'
    db = mysqlDriver.connect(host = Hostdb, user = Userdb, passwd = Passdb, db=nameDB)
    cur = db.cursor()
    time_now = time.strftime("%Y-%m-%d %H:%M:%S")
    time.sleep(30)
    time_finished = time.strftime("%Y-%m-%d %H:%M:%S")
    query = """ 
    insert into senslopedb.dummy_table (output,time_start,time_end) values (%s,'%s','%s')
    """ %(int(write),str(time_now),str(time_finished))
    cur.execute(query)
    db.commit()    
    print query

if __name__ == "__main__":
    main()