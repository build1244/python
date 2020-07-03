from flask import Flask
from flask import Response
from flask import request
from redis import Redis
from datetime import datetime
import json
import MySQLdb
import time

checkdb = 0
while checkdb == 0:
    try:
        db = MySQLdb.Connect("mysql-db","root","password")
    except:
        time.sleep(2)
	continue
    else:
	checkdb = 1


