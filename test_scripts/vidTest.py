import cv2
import numpy as np
import sys, getopt

if __name__ == '__main__':
	print(__doc__)

	args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade='])
	try:
		video_src = video_src[0]
	except:
		print("No video source supplied.")
		exit()
	args = dict(args)
	cascade_fn = args.get('--cascade', "cascade_dir/cascade.xml")

	car_cascade = cv2.CascadeClassifier(cascade_fn)
	cap = cv2.VideoCapture(video_src)

	paused = False
	step = True

	while True:
		if not paused or step:
			flag, img = cap.read()
			if img is None:
				break
			img = cv2.resize(img, (540, 1144))
			height, width, c = img.shape
			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			cars = car_cascade.detectMultiScale(gray, 1.2, 5)

			for (x,y,w,h) in cars:
				cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2) 

			cv2.imshow('edge', img)

			sub_face = img[y:y+h, x:x+w]
			FaceFileName = "cropped_plate/plate_" + str(y+x) + ".jpg" # folder path and random name image
			cv2.imwrite(FaceFileName, sub_face)

		step = False
		ch = cv2.waitKey(5)
		if ch == 13:
			step = True
		if ch == 32:
			paused = not paused
		if ch == 27:
			break
	cv2.destroyAllWindows()