#!/usr/bin/python3

import pymysql

# Open database connection
db = pymysql.connect("localhost","chatbot","chatbot","BOTDB" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = """INSERT INTO shops(id,
   name, passwd , counter)
   VALUES (6, 'doublecheese',6, 12)"""
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

# disconnect from server
db.close()
