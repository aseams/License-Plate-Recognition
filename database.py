import pymysql as pms
import sys
import dbConn

def connect():
	"""
	Connects Python to local database with login info from dbConn.py
	"""
	connection = pms.connect(host=dbConn.host, user=dbConn.user, password=dbConn.passwd, database=dbConn.database, autocommit=True)
	global cursor
	cursor = connection.cursor()

def close():
	"""
	Closes database connection
	"""
	connection.close()

def insert(plate, state="", comment=""):
	"""
	Used to insert rrecords into database table
	"""
	try:
		connection.ping()
	except:
		connect()
	image = (plate.lower() + ".png")
	try:
		query = "INSERT INTO captures(plate_no, state, image, comment) VALUES ('{0}', '{1}', '{2}', '{3}');".format(plate.upper(), state, image, comment)
	except:
		print("Error with query")

	try:
		cursor.execute(query)
	except:
		print("Error with execution")

def select():
	"""
	Used to select all records in the table. Currently not used.
	"""
	query = "select * from captures;"
	rows = cursor.fetchall()
	for row in rows:
		print(row)