#initial setup
import sqlite3

def executefile(fn,con):
	f = open(fn)
	cur = con.cursor()
	commands = f.read().split(';')
	f.close()
	for command in commands:
		try:
			cur.execute(command);
			print "Successfully executed - " + command
			con.commit()
		except:
			print "Failed for " + command
			con.rollback()
	print "File executed"

con = sqlite3.connect("att_man")

