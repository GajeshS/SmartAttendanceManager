import db

l = db.login()
l.get()
x = l.Auth()
if x == 'admin':
	a = db.admin()
	while True:
		print " Press 1 to add member \n2 to remove member"
		i = raw_input("")
		if i not in ['1','2']:
			break
		elif i == '1':
			a.add()
		else :
			i = (int)(raw_input("enter ID of student to remove: "))
			a.rem(i)
elif x == 'student':
	s = db.student(l)
	s.view()

elif x == 'teacher':
	t = db.teacher(l)
	print "press any key to start and esc to leave"
	q=db.getch()
	t.recog()
	
else :
	print "invalid login"
