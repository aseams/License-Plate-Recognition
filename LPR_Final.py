import glob
import os
import re
import sys
import requests
import json

import cv2
import numpy as np
from PIL import Image, ImageFilter
from pyocr import builders, pyocr

import constants

# Params for Pre-Processing
ADAPTIVE_THRESH_BLOCK_SIZE = constants.ADAPTIVE_THRESH_BLOCK_SIZE
ADAPTIVE_THRESH_WEIGHT = constants.ADAPTIVE_THRESH_WEIGHT

# Params for Plate Detection
SML_CTR_MIN_RATIO = constants.SML_CTR_MIN_RATIO
SML_CTR_MAX_RATIO = constants.SML_CTR_MAX_RATIO
PLATE_MAX_ASPECT_RATIO = constants.PLATE_MAX_ASPECT_RATIO
CTR_MIN_EXTENT_RATIO = constants.CTR_MIN_EXTENT_RATIO





def writeToFile():
	cv2.imwrite(filepath, filename)

def run_once(input_file):
	dirs = ['detection', 'plate', 'preprocess']
	for folder in dirs:
		ensure_dir(folder)
	print("Procesing {0}".format(input_file))
	img = cv2.imread(input_file)
	bilateral, preprocessed_image = preprocesss(img)
	writeToFile("bilateral.jpg", bilateral)
	writeToFile("preprocess/{}.jpg".format(input_file), preprocessed_image)
	img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	writeToFile("preprocess/img_gray.jpg", img_gray)
	thresh1 = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,15,2)
	writeToFile("preprocess/thresholded.jpg", thresh1)
	denoised_image = cv2.fastNlMeansDenoising(thresh1)
	writeToFile("preprocess/denoised.jpg", denoised_image)
	img_gray = find_plate_rectangle(img_gray)
	denoised = find_plate_rectangle(denoised_image)
	threshold = find_plate_rectangle(thresh1)
	detected_plate = {
		"img_gray": img_gray,
		"threshold": threshold,
		"denoised": deniosed
	}
	# print('detected_plate: \n' + str(detected_plate))
	# print('preprocessed_image: \n' + str(preprocessed_image))
	# ocr_text = extract_plate_value(detected_plate[-1],
	# 							   img, input_file,
	# 							   "detection",
	# 							   "plate")
	# print('ocr_text: ' + str(ocr_text))
	ocr_text = ocr_space_file(constants.input_file, constants.overlay, constants.api_key, constants.language, constants.OCREngine)
	print('ocr_text: ' + json.dumps(ocr_text, indent = 2))

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