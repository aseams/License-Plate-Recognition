import cv2
import numpy as np
import pytesseract
from PIL import Image
import argparse
import re
import constants

def get_string(pic_path):
	# Reading picture with opencv
	pic = cv2.imread(pic_path)
	cv2.imshow("original", pic)
	# grey-scale the picture
	pic = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
	cv2.imshow("grayscale", pic)
	# Do dilation and erosion to eliminate unwanted noises
	kernel = np.ones((1, 1), np.uint8)
	pic = cv2.dilate(pic, kernel, iterations=20)
	cv2.imshow("dilate", pic)
	pic = cv2.erode(pic, kernel, iterations=20)
	cv2.imshow("erode", pic)
	# Write image after removed noise
	cv2.imwrite(plate + "_no_noise.png", pic)
	#  threshold applying to get only black and white picture 
	pic = cv2.adaptiveThreshold(pic, 300, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
	cv2.imshow("threshold", pic)
	# Write the image for later recognition process 
	cv2.imwrite(plate + "_threshold.png", pic)
	# Character recognition with tesseract
	#final = pytesseract.image_to_string(Image.open(plate + "_threshold.png"))
	final = pytesseract.image_to_string(Image.open("plate_344.jpg"))
	return final

# string1 = get_string(plate)
# print(string1)
# cv2.waitKey(0)
# print("\n\n\n")
print(pytesseract.image_to_string(Image.open("veh_1323.jpg")))

# string2 = pytesseract.image_to_string(Image.open("plate_344.jpg"))
# print(string2)
# string2 = re.sub(r"\. |[^\w\.\* ]| \.| (?=/)", "", string2)
# string2 = list(string2.split(" "))
# print(string2)

# string2 = pytesseract.image_to_string(Image.open("LICENSE_PLATE.PNG"))
# if any(state in string2 for state in state_names):
#     print(string2)

# print("\n\n\n")
# print(string2)