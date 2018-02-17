#! /usr/bin/env python

import cgi
import cgitb
import Cookie, os, inspect, subprocess
cgitb.enable()
import mysql.connector as conn
import random
# add parent dir path to sys.path
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
UPLOAD_DIR = parentdir + '/image'

db = conn.connect(host='172.30.241.99', user='root', passwd='root', db='exampledb')
cursor = db.cursor()
success = False


print "Content-type: text/html\n\n"
print '''
<html>
<head>
'''

print '''
<title>Uploading</title>
</head>
<body>
'''

try:
	cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])

	hit_count_path = os.path.join(os.path.dirname(__file__), "hit-count.txt")

	if os.path.isfile(hit_count_path):
	    hit_count = int(open(hit_count_path).read())
	    hit_count += 1
	else:
	    hit_count = 1

	hit_counter_file = open(hit_count_path, 'w')
	hit_counter_file.write(str(hit_count))
	hit_counter_file.close()

	form = cgi.FieldStorage()
	form_file = form['file']
	privatee = form.getvalue('private')
	extension = form_file.filename.split('.')
	f = str(hit_count) + '.' + str(extension[1])
	uploaded_file_path = os.path.join(UPLOAD_DIR, f)
	print '{0}<br>'.format(cgi.escape(str(uploaded_file_path)))

	with file(uploaded_file_path, 'wb') as fout:
		print '1 try<br>'
		while True:
			chunk = form_file.file.read(100000)
			if not chunk:
				break
			fout.write (chunk)

	try:
		command = ["magick", "identify", uploaded_file_path]
		process = subprocess.Popen(command, stdout=subprocess.PIPE)
		print '2 try<br>'
		output, err = process.communicate()
		print '2 try 2<br>'
		h = output.split(" ")
		if h[1].lower() == "jpeg":
			h[1] = "JPG"
		print '{0} {1}'.format(cgi.escape(str(h[1].lower()), str(extension[1])))
		if (h[1].lower() != extension[1]):
			os.remove(uploaded_file_path)
			hit_count = int(open(hit_count_path).read())
			hit_count -= 1
			hit_counter_file = open(hit_count_path, 'w')
			hit_counter_file.write(str(hit_count))
			hit_counter_file.close()
		else:
			g = h[2].split("x")
			sql = "insert into image(file_name, username, private, permlink, width, height) values('%s','%s', '%d', '%d', '%d', '%d')" % (f, cookie["username"].value, int(privatee), 0, int(g[0]), int(g[1]))
			cursor.execute(sql)
			db.commit()
			success = True
	except:
		print '2 except<br>'
		os.remove(uploaded_file_path)
		hit_count = int(open(hit_count_path).read())
		hit_count -= 1
		hit_counter_file = open(hit_count_path, 'w')
		hit_counter_file.write(str(hit_count))
		hit_counter_file.close()
	j = 1
except:
	print '1 except<br>'
	j = 0

cursor.close()

print 'done<br>'
print '</body>'
print '</html>'

