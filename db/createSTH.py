import sys
import MySQLdb
import datetime

def recurInsert():
	db = MySQLdb.connect(host="localhost", user="root", passwd="", db="testForum", charset="utf8")
	cursor = db.cursor()

	sql1 = "SET GLOBAL temp_id1 = 0;"
	cursor.execute(sql1)

	for i in range(50):
		test_name = "testUser" + str(i) 
		temp_sql = "CALL ADD_NEWUSER( '" + test_name + "', 'root', '', 'male', '', '2019-1-4', temp_id1); "
		cursor.execute(temp_sql)

if __name__ == "__main__":
	recurInsert()