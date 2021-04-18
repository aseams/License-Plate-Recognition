import pymysql as pms
import sys
import dbConn

def connect():
	connection = pms.connect(host=dbConn.host, user=dbConn.user, password=dbConn.passwd, database=dbConn.database, autocommit=True)
	global cursor
	cursor = connection.cursor()

def close():
	connection.close()

def insert(plate, comment):
	try:
		connection.ping()
	except:
		connect()
	image = (plate.lower() + ".png")
	state = ""
	try:
		query = "INSERT INTO captures(plate_no, state, image, comment) VALUES ('{0}', '{1}', '{2}', '{3}');".format(plate.upper(), state, image, comment)
	except:
		print("Error with query")

	try:
		cursor.execute(query)
	except:
		print("Error with execution")

def select():
	query = "select * from captures;"
	rows = cursor.fetchall()
	for row in rows:
		print(row)