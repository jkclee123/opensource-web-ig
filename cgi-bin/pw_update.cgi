#! /usr/bin/env python

import cgi
import cgitb
cgitb.enable()
import mysql.connector as conn
import Cookie, os
import datetime
import random

def connectDB():
	db = conn.connect(host='172.30.241.99', user='root', passwd='root', db='exampledb')
	cursor = db.cursor()
	return db, cursor
	
def editPeople(db, cursor, username, password):
	sql = "update account set password = '%s' where account.username = '%s'" % (password, username)
	cursor.execute(sql)
	db.commit()
	return

form = cgi.FieldStorage()
password = form.getvalue("password")
re_password = form.getvalue("re_password")
db, cursor = connectDB()

try:
	cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
	expiration = datetime.datetime.now() + datetime.timedelta(days=30)
	sql = "select username from account where username = '%s' and password = '%s'"%(cookie["username"].value, cookie["password"].value)
	cursor.execute(sql)
	ac = cursor.fetchall()
	if ac != [] and password == re_password and password != None:
		editPeople(db, cursor, cookie["username"].value, password)
		cookie["username"]["expires"] = 'Thu, 01 Jan 1970 00:00:00 GMT'
		cookie["password"]["expires"] = 'Thu, 01 Jan 1970 00:00:00 GMT'
		c1 = Cookie.SimpleCookie()
		c2 = Cookie.SimpleCookie()
		c1["username"] = cookie["username"].value
		c1["username"]["expires"] = \
		expiration.strftime("%a %d-%b-%Y %H:%M:%S PST")
		c1["username"]["path"] = '/'
		c2["password"] = password
		c2["password"]["expires"] = \
		expiration.strftime("%a %d-%b-%Y %H:%M:%S PST")
		c2["password"]["path"] = '/'
		print c1 
		print c2	
		j = 1
		message = ""
	else:
		message = "Invalid username or password!"
except(Cookie.CookieError, KeyError):
	j = 0
	
html ='''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta http-equiv="refresh" content="0;url=/cgi-bin/index.cgi?message={0}" />
  <title>Processing</title>
</head>
<body>
</body>
</html>
'''.format(cgi.escape(message))

cursor.close()
print "Content-type: text/html\n\n" + html