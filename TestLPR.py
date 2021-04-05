import glob
import os
import re
import sys

import cv2
import numpy as np
from PIL import Image, ImageFilter
from pyocr import builders, pyocr

import constants

def preprocesss(img, color=True):
	#print('preprocess()')
	# Pre-processing of image as follows:
	# 1. Convert to Gray Scale
	# 2. Histogram Equalization
	# 3. Image Blur (Smoothing) using 1x1 kernel
	# 4. Apply Bilateral Filter
	if color:
		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	else:
		img_gray = img
	img_gray = cv2.equalizeHist(img_gray)
	#img_gray = cv2.blur(img_gray, (3, 3))
	img_gray = cv2.bilateralFilter(img_gray, 11, 17, 17)
	bilateral = img_gray
	return bilateral, cv2.adaptiveThreshold(img_gray, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)

def find_plate_rectangle(img):
	# print('find_plate_rectangle()')
	# This function finds plate in the image.
	# The idea is to find a rectangle within the image

	contours, method = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)

	contours = [c for c in contours
				if cv2.contourArea(c) > img.size * SML_CTR_MIN_RATIO
				and cv2.contourArea(c) < img.size * SML_CTR_MAX_RATIO]
	ret = []
	for c in contours:
		peri = cv2.arcLength(c, True)
		## 0.02 is epsilon
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		if len(approx) == 4:
			x, y, w, h = cv2.boundingRect(approx)
			area = cv2.contourArea(c)
			rect_area = w * h
			extent = float(area) / rect_area
			aspect_ratio = float(w) / h
			if extent > CTR_MIN_EXTENT_RATIO and aspect_ratio < PLATE_MAX_ASPECT_RATIO:
				ret.append(approx)
	return ret

def extract_plate_value(plateContour, img, plate_id, plate_detected_location, plate_location):
	# print('extract_plate_value()')
	if plateContour is not None:
		x, y, w, h = cv2.boundingRect(plateContour)
		crop = img[y:y + h, x:x + w]
		crop = cv2.resize(crop, (0, 0), fx=4, fy=4)
		hsv = preprocess_ocr(crop)
#		hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
		print('loc: ' + plate_location)
		print('id: ' + plate_id)
		cv2.imwrite('{}/{}.jpg'.format(plate_location, plate_id), hsv)
		im = Image.open('{}/{}.jpg'.format(plate_location, plate_id))
		# cv2.imwrite('plates/{}'.format(plate_id), hsv)
		# im = Image.open('plates/{}'.format(plate_id))
		im.filter(ImageFilter.SHARPEN)
		cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
		# print('loc: ' + plate_detected_location)
		# print('id: ' + plate_id)
		cv2.imwrite('./{}/{}.jpg'.format(plate_detected_location,
										 plate_id),
					img)
		return ocr_plate(im)

def preprocess_ocr(img):
	#print('preprocess_ocr()')
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img_edg = cv2.Canny(img, 0, 100)
	structuring_element = cv2.getStructuringElement(cv2.MORPH_DILATE, (6, 6))
	morfo = cv2.dilate(img_edg, structuring_element, iterations=1)
	return morfo


def ocr_plate(im):
	#print('ocr_plate()')
	tool = pyocr.get_available_tools()[0]
	txt = tool.image_to_string(im)
	return txt


def run_aplr(input_location, preprocess_location, plate_detected_location, plate_location):
	for image in glob.glob("{0}/*.png".format(input_location)):
		# print('in: ' + input_location)
		# print('pre: ' + preprocess_location)
		# print('det: ' + plate_detected_location)
		# print('loc: ' + plate_location)
		image = image.replace('\\', '/')
		print('img: ' + image)
		img = cv2.imread(image)
		preprocessed_image = preprocesss(img)
		idx = image.split("/")[-1].split(".")[0]
		# print('pre: ' + format(preprocess_location,idx))
		# print('pre: ' + preprocessed_image)
		cv2.imwrite("{0}/{1}.jpg".format(preprocess_location,
										 idx), preprocessed_image)
		detected_plate = find_plate_rectangle(preprocessed_image)
		#if detected_plate:
		try:
			ocr_text = extract_plate_value(detected_plate[-1],
										   img, idx,
										   plate_detected_location,
										   plate_location)

			print(ocr_text)
		except:
			print('error')

def run_once(input_file):
	dirs = ['detection', 'plate', 'preprocess']
	for folder in dirs:
		ensure_dir(folder)
	print("Procesing {0}".format(input_file))
	img = cv2.imread(input_file)
	bilateral, preprocessed_image = preprocesss(img)
	cv2.imwrite("bilateral.jpg", bilateral)
	#sys.exit(0)
	#print('idx: ' + idx)
	cv2.imwrite("preprocess/{}.jpg".format(input_file), preprocessed_image)
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	cv2.imwrite("preprocess/img_gray.jpg", img_gray)
	thresh1 = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,2)
	cv2.imwrite("preprocess/thresholded.jpg", thresh1)
	denoised_image = cv2.fastNlMeansDenoising(thresh1)
	cv2.imwrite("preprocess/denoised.jpg", denoised_image)
	detected_plate = find_plate_rectangle(denoised_image)
	if detected_plate:
		# print('detected_plate: \n' + str(detected_plate))
		# print('preprocessed_image: \n' + str(preprocessed_image))
		ocr_text = extract_plate_value(detected_plate[-1],
									   img, input_file,
									   "detection",
									   "plate")
		# print('ocr_text: ' + str(ocr_text))
		print('ocr_text: ' + str(ocr_text))
		ocr_text = re.split('[\n,.=}]',ocr_text)
		print('ocr_text_split: ' + str(ocr_text))
		ocr_text = [word for word in ocr_text if len(word) in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]]
		print('ocr_text_len: ' + str(ocr_text))
		if " " in ocr_text[0]:
			state = ocr_text[0].strip()
		else:
			state = ocr_text[0]

		if " " in ocr_text[1]:
			plate = ocr_text[1].strip()
		else:
			plate = ocr_text[1]
		# print('ocr_text_final: ' + str(ocr_text))
		state = stateExists(state)
		if state == "error":
			sys.exit("\nState not found/confirmed")
		if confirmDB(state, plate):
			print("Adding " + state + ":" + plate + " to database")
		else:
			print("Skipped adding " + state + ":" + plate + " to database.")
		#print("Plate is: {0}".format(ocr_text.split("\n")[4]))
		#print("Plate is: {}".format(ocr_text.split("; |, |\n")[4]))

def stateExists(state):
	state_names = ["Alaska", "Alabama", "Arkansas", "American Samoa", 
				   "Arizona", "California", "Colorado", "Connecticut", 
				   "District of Columbia", "Delaware", "Florida", 
				   "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", 
				   "Illinois", "Indiana", "Kansas", "Kentucky", 
				   "Louisiana", "Massachusetts", "Maryland", "Maine", 
				   "Michigan", "Minnesota", "Missouri", "Mississippi", 
				   "Montana", "North Carolina", "North Dakota", 
				   "Nebraska", "New Hampshire", "New Jersey", 
				   "New Mexico", "Nevada", "New York", "Ohio", 
				   "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", 
				   "Rhode Island", "South Carolina", "South Dakota", 
				   "Tennessee", "Texas", "Utah", "Virginia", 
				   "Virgin Islands", "Vermont", "Washington", "Wisconsin", 
				   "West Virginia", "Wyoming"]

	common_issues = {"":"Alaska", "":"Alabama", "":"Arkansas", "":"American Samoa", 
				   "":"Arizona", "IN Cn bijouvia":"California", "":"Colorado", "":"Connecticut", 
				   "":"District of Columbia", "":"Delaware", "":"Florida", 
				   "":"Georgia", "":"Guam", "":"Hawaii", "":"Iowa", "":"Idaho", 
				   "":"Illinois", "":"Indiana", "":"Kansas", "":"Kentucky", 
				   "":"Louisiana", "":"Massachusetts", "":"Maryland", "":"Maine", 
				   "":"Michigan", "":"Minnesota", "":"Missouri", "":"Mississippi", 
				   "":"Montana", "":"North Carolina", "":"North Dakota", 
				   "":"Nebraska", "":"New Hampshire", "":"New Jersey", 
				   "":"New Mexico", "":"Nevada", "":"New York", "":"Ohio", 
				   "":"Oklahoma", "":"Oregon", "":"Pennsylvania", "":"Puerto Rico", 
				   "":"Rhode Island", "":"South Carolina", "":"South Dakota", 
				   "":"Tennessee", "":"Texas", "":"Utah", "":"Virginia", 
				   "":"Virgin Islands", "":"Vermont", "":"Washington", "":"Wisconsin", 
				   "":"West Virginia", "":"Wyoming"}

	state_abrv  = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE",
				   "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", 
				   "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", 
				   "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", 
				   "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", 
				   "VT", "VA", "WA", "WV", "WI", "WY"]
	if state in state_names:
		return state
	elif state in state_abrv:
		return state
	elif state in common_issues:
		return str(common_issues.get(state))
	else:
		return "error"

def ensure_dir(file_path):
	directory = os.path.realpath(file_path)
	if not os.path.exists(directory):
		print('Creating directory: ' + os.path.basename(directory))
		os.makedirs(directory)

def confirmDB(state, plate):
	valid = {"yes": True, "y": True, "ye": True,
			 "no": False, "n": False}
	prompt = " [y/n] "

	while True:
		print("Add " + state + ":" + plate + " to database? " + prompt)
		#sys.stdout.write(question + prompt)
		choice = input().lower()

		if choice in valid:
			return valid[choice]
		else:
			print("Please respond with 'yes' or 'no' "
							 "(or 'y' or 'n').\n")

if __name__ == '__main__':
	args = sys.argv[1:]

	if len(args) != 1 and len(args) != 4:
		print('Usage: python TestLPR.py [input] [preprocessed images] [detections] [plates]')
		print('[input] required. Can be file or folder.')
		print('[preprocessed_images] is a folder')
		print('[detections] is a folder')
		print('[plates] is a folder')
		sys.exit()


	if len(args) == 4:
		inputFile = sys.argv[1]
		preprocess = sys.argv[2]
		detection = sys.argv[3]
		plates = sys.argv[4]

		if not os.path.exists(f'{inputFile}'):
			os.makedirs(f'{inputFile}')

		if not os.path.exists(preprocess):
			print(f'creating directory: {preprocess}')
			os.makedirs(preprocess)

		if not os.path.exists(detection):
			os.makedirs(detection)

		if not os.path.exists(plates):
			os.makedirs(plates)
		run_aplr(inputFile, preprocess, detection, plates)

	else:
		run_once(sys.argv[1]) #Usage: python testLPR.py [file]




	# if len(userInput) == 1:
	# 	filename = userInput[0]
	# 	run_once(filename) #Usage: python testLPR.py [file]
	# 	# print(filename)
	# elif len(userInput) == 4:
	# 	image = userInput[0]
	# 	preprocess = userInput[1]
	# 	detection = userInput[2]
	# 	plate = userInput[3]
	# 	run_aplr(
	# 		image,
	# 		preprocess,
	# 		detection,
	# 		plate
	# 	)
		# run_aplr(
		#  "D:/andys/Documents/Kean University/4 Spring 2021/Senior Project/all_TestLPR/input_images", 
		#  "D:/andys/Documents/Kean University/4 Spring 2021/Senior Project/all_TestLPR/preprocessed", 
		#  "D:/andys/Documents/Kean University/4 Spring 2021/Senior Project/all_TestLPR/detected",
		#  "D:/andys/Documents/Kean University/4 Spring 2021/Senior Project/all_TestLPR/plates"
		# )
