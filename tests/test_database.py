import sqlite3
from config import *

try:
	connection = sqlite3.connect(DATABASE)
	cursor.connection.cursor()
	cursor.execute("SELECT sqlite_verion();")
	version-cursor.fetchdone()
	print(version)
	connection.close()
	print("Database OK")
except Exception as e:
	print(e)
