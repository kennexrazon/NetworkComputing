# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 09:39:25 2017

@author: chocolate server
"""

import MySQLdb as mysqlDriver

Hostdb = '127.0.0.1'
Userdb = 'root'
Passdb = 'senslope'
nameDB = 'senslopedb'
db = mysqlDriver.connect(host = Hostdb, user = Userdb, passwd = Passdb, db=nameDB)
cur = db.cursor()