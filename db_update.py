#!/usr/bin/python3

import pymysql
db = pymysql.connect("localhost","chatbot","chatbot","BOTDB" )
# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to UPDATE required records
sql = "UPDATE shops SET counter = 10 \
                        WHERE name = 'tasty'"
       
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