# -*- coding: utf-8 -*-
#!/usr/bin/python
import pymysql
import datetime


db = pymysql.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="",  # your password
                     db="tweet")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()
now = datetime.datetime(2018, 5, 31)

try:
  with db.cursor() as cursor:
      sql = 'INSERT INTO posts (text, created) VALUES (%s, %s)'
      cursor.execute(sql, ('tsetsetsfsdfset', now))
  db.commit()
  print(cursor.lastrowid)
  # 1 (last insert id)

  # Use all the SQL you like
  cur.execute("SELECT * FROM posts")

  # print all the first cell of all the rows
  for row in cur.fetchall():
    print(row[1])

finally:
  db.close()

