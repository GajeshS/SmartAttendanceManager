import sqlite3,reco,data,os

class getch:
    def __init__(self):
        self.call()

    def call(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class student:
	func=['view']
	def __init__(self,obj):
		self.con=sqlite3.connect("att_man")
		self.cur = self.con.cursor()
		self.rollno = obj.uname
		rs = self.cur.execute('''select * from student where RollNo=? ''',(obj.uname,))
		x = rs.fetchone()
		a = self.cur.execute('''select count(*) from attendance;''')
		b = self.cur.execute('''select count(*) from attendance where ID =?;''',(self.rollno,))
		
		self.name = x[0].encode()
		self.percentage = (float)(b.fetchone())/(float)(a.fetchone())
		
		
	def view(self):
		#display the details in UI
		print "Name : " + self.name
		print "Roll No. : " + self.rollno
		print "Attendance : " + self.percentage
		
class teacher:
	func = ['recog']
	def __init__(self,obj):
		self.con=sqlite3.connect("att_man")
		self.cur = self.con.cursor()
		self.rollno = obj.uname
		rs =self.cur.execute('''select * from teacher where RollNo=? ''',(obj.uname,))
		x = rs.fetchone()
		self.name = x[0].encode()
		self.subject = x[2].encode()
		
	def recog(self):
		x = reco.recognize()
		y = len(x)
		x = [((int)(i),) for i in x]
		self.cur.execute("""insert into subject_timings values(date('now','localtime'), strftime('%H','now','localtime') ,?,?); """,(self.subject.decode(),y)) 
		self.cur.executemany("""insert into attendance values(date('now','localtime') , strftime('%H','now','localtime') , ? );""",x)
		self.con.commit()
	def strength():
		rs = self.cur.execute('''select * from subject_timings where TeacherID =? order by Today,c_hour;''',(self.rollno,) )
		#print "Attendance so far :" 
		try:
			x = rs.fetchall()
			print "Attendance so far :"
			for i in x:
				print x[0]+" "+x[1]+" "+x[2]
		except:
			print "unexpected error occurred"
		
	
	
class login:
	func = ['get','getu','getp','readu','readp','Auth']
	
	def __init__(self):
		self.con=sqlite3.connect("att_man")
		self.cur = self.con.cursor()
		
	def get(self):
		self.uname=(int)(raw_input("Enter user ID: "))
		self.pwd = raw_input("Enter Password: ")
		
	def getu(self,name):
		self.uname=name
	def getp(self,pas):
		self.pwd = pas
	def readu(self):
		self.uname =(int)(raw_input("Enter user ID: "))
	def readp(self):
		self.pwd = raw_input("Enter Password: ")
	def add(self,axs):
		self.cur.execute('''insert into login values (?,?,?); ''',(self.uname,self.pwd.decode(),axs.decode()))
		self.con.commit()
	def Auth(self):
		try:
			rs = self.cur.execute('''select * from login where ID=? and Pass=?;''',(self.uname,self.pwd.decode()))
			x = rs.fetchone()
			self.axs= x[2].encode()
			r = self.axs
		except:
			r = "__hacker__"
			pass
		return r
		
	
class admin:
	
	def __init__(self):
		self.con=sqlite3.connect("att_man")
		self.cur = self.con.cursor()
		#self.rollno = obj.uname
		
	def add(self):
		l = login()
		l.get()
		axs = raw_input("Access Spec of new user :")
		if axs not in ['student','teacher']:
			print "Access not part of allowed set"
			return
		elif axs == 'student':
			#s = student()
			l.add(axs)
			nam = raw_input("Enter Student's name:")
			self.cur.execute('''insert into student values (?,?); ''',(nam.decode(),l.uname))
			data.train(l.uname)
			self.con.commit()
		else:
			#s = teacher()
			nam = raw_input("Enter teacher's name:")
			sub = raw_input("Enter teacher's subject:")
			l.add(axs)
			self.cur.execute('''insert into teacher values (?,?,?); ''',(nam.decode(),l.uname,sub.decode()))
			self.con.commit()
			
	def rem(self,ID):
		rs = self.cur.execute('''select acces from login where ID=?; ''',(ID,))
		try:
			x = rs.fetchone()
			if x[0]=='teacher':
				self.cur.execute('''delete from login where ID=?;''',(ID,))
				print "1"
				self.cur.execute('''delete from teacher where RollNo = ?;''',(ID,))
				print "1"
				self.con.commit()
			elif x[0]=='student':
				print "student"
				self.cur.execute('''delete from login where ID=?;''',(ID,))
				print "1"
				self.cur.execute('''delete from student where RollNo = ?;''',(ID,))
				print "1"
				os.system("rm -r data/data/"+str(ID))
				print "1"
				self.con.commit()
				print "removed"
				
		except:
			self.con.rollback()
