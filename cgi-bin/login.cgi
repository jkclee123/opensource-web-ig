#! /usr/bin/env python
import cgi
import cgitb
cgitb.enable()
import mysql.connector as conn
import Cookie
import datetime
import random


form = cgi.FieldStorage()
username = form.getvalue("username")
password = form.getvalue("password")
db = conn.connect(host='172.30.241.99', user='root', passwd='root', db='exampledb')
cursor = db.cursor()
sql = "select username from account where username = '%s' and password = '%s'"%(username, password)
cursor.execute(sql)
ac = cursor.fetchall()
cursor.close()

if ac != []:
	expiration = datetime.datetime.now() + datetime.timedelta(days=30)
	c1 = Cookie.SimpleCookie()
	c2 = Cookie.SimpleCookie()
	c3 = Cookie.SimpleCookie()
	c1["username"] = username
	c1["username"]["expires"] = \
	expiration.strftime("%a %d-%b-%Y %H:%M:%S PST")
	c1["username"]["path"] = '/'
	c2["password"] = password
	c2["password"]["expires"] = \
	expiration.strftime("%a %d-%b-%Y %H:%M:%S PST")
	c2["password"]["path"] = '/'
	print c1 
	print c2
	message = ""
else:
	message = "Invalid username or password!"

html ='''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta http-equiv="refresh" content="0;url=http:/cgi-bin/index.cgi?message={0}" />
  <title>Processing...</title>
</head>
<body>
</body>
</html>
'''.format(cgi.escape(message))

print "Content-type: text/html\n\n" + html