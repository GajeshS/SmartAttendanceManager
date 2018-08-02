import cv2, numpy, os, sqlite3

haar_file = 'data/face.xml'
datasets = 'data/data' 

def train(obj):
	
	sub_data =  str(obj)

	path = os.path.join(datasets, sub_data)
	if not os.path.isdir(path):
	    os.mkdir(path)
	model = cv2.face.createFisherFaceRecognizer()
	(width, height) = (130, 100)
	try:		
		model.load('data/rec.xml')
	except:
		print('Rebuilding the recognizer. This may take a moment.')
		# Create a list of images and a list of corresponding names
		(images, lables, names, id) = ([], [], {}, 0)
		for (subdirs, dirs, files) in os.walk(datasets):
		    for subdir in dirs:
			names[id] = subdir
			subjectpath = os.path.join(datasets, subdir)
			for filename in os.listdir(subjectpath):
			    path = subjectpath + '/' + filename
			    lable = id
			    images.append(cv2.imread(path, 0))
			    lables.append(int(subdir))
			id += 1
		

		# Create a Numpy array from the two lists above
		(images, lables) = [numpy.array(lis) for lis in [images, lables]]
		frec.train(images, lables)
		frec.save('data/rec.xml')


	face_cascade = cv2.CascadeClassifier(haar_file)
	webcam = cv2.VideoCapture(0)
	imgs = list()
	labs=list()
	count = 1
	while count < 50: 
	    (_, im) = webcam.read()
	    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	    faces = face_cascade.detectMultiScale(gray, 1.3, 4)
	    for (x,y,w,h) in faces:
		cv2.rectangle(im,(x,y),(x+w,y+h),(255,0,0),2)
		face = gray[y:y + h, x:x + w]
		face_resize = cv2.resize(face, (width, height))
		cv2.imwrite('%s/%s.png' % (path,count), face_resize)
	    	count += 1
		imgs.append(face_resize)
		labs.append(sub_data)
	    cv2.imshow('OpenCV', im)
	    
	    key = cv2.waitKey(10)
	    if key == 27:
	    	frec.update(imgs,labs)
	    	frec.save('data/rec.xml')
		break
	
	cv2.destroyAllWindows()
