import numpy as np
import cv2
import imutils
import sys
import pytesseract
import pandas as pd
import time
import glob
from pathlib import Path


def main():
	extensions = ['.jpg', '.png', '.jpeg']
	images = [x for x in Path('D:/andys/Documents/Kean University/4 Spring 2021/Senior Project/ProjCode/RESTART/cropped_vehicle/upscaled').iterdir() if x.suffix.lower() in extensions]
	# print(images)
	# input_location = "D:/andys/Documents/Kean University/4 Spring 2021/Senior Project/ProjCode/RESTART/OPENCV-LICENSE-PLATE-RECOGNITION-SYSTEM-master/TEST_IMAGES"
	#for img in glob.glob("{0}/*.png".format(input_location)):
	for img in images:
		image = cv2.imread(str(img))
		image = imutils.resize(image, width=500)
		#cv2.imshow("Original Image", image)
		preprocessing(image)

def preprocessing(image):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	#cv2.imshow("1 - Grayscale Conversion", gray)
	grey = cv2.bilateralFilter(gray, 11, 17, 17)
	#cv2.imshow("2 - Bilateral Filter", gray)
	edged = cv2.Canny(gray, 170, 200)
	#cv2.imshow("4 - Canny Edges", edged)
	hori = np.concatenate((gray, grey, edged),axis=1)
	cv2.imshow("Preprocess", hori)
	cv2.waitKey(5000)
	contours(edged,image,gray)

def contours(edged,image,gray):
	
	cv2.destroyWindow("Preprocess")

	cnts, new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:30]
	NumberPlateCnt = None 

	count = 0
	for c in cnts:
	        peri = cv2.arcLength(c, True)
	        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
	        if len(approx) == 4:  
	            NumberPlateCnt = approx 
	            break
	masking(NumberPlateCnt,image,gray)

def masking(NumberPlateCnt,image,gray):
	# Masking the part other than the number plate
	mask = np.zeros(gray.shape,np.uint8)
	new_image = cv2.drawContours(mask,[NumberPlateCnt],0,255,-1)
	new_image = cv2.bitwise_and(image,image,mask=mask)
	#cv2.namedWindow("Final_image",cv2.WINDOW_NORMAL)
	cv2.imshow("Final_image",new_image)
	cv2.waitKey(5000)
	cv2.destroyAllWindows()
	getChars(new_image)

def getChars(new_image):
	# Configuration for tesseract
	config = ('-l eng --oem 1 --psm 3')

	# Run tesseract OCR on image
	text = pytesseract.image_to_string(new_image, config=config)

	#Data is stored in CSV file
	raw_data = {'date': [time.asctime( time.localtime(time.time()) )], 
	        'v_number': [text]}

	df = pd.DataFrame(raw_data, columns = ['date', 'v_number'])
	df.to_csv('data.csv')

	# Print recognized text
	print(text)

	cv2.waitKey(0)

main()