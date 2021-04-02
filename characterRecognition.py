import cv2
import numpy as np
import pytesseract
from PIL import Image
import argparse
import re

# Path of image
main_path = r'Typeface.png'
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

def get_string(pic_path):
	# Reading picture with opencv
	pic = cv2.imread(pic_path)
	# grey-scale the picture
	pic = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
	# Do dilation and erosion to eliminate unwanted noises
	kernel = np.ones((1, 1), np.uint8)
	pic = cv2.dilate(pic, kernel, iterations=20)
	pic = cv2.erode(pic, kernel, iterations=20)
	# Write image after removed noise
	cv2.imwrite(main_path + "no_noise.png", pic)
	#  threshold applying to get only black and white picture 
	pic = cv2.adaptiveThreshold(pic, 300, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
	# Write the image for later recognition process 
	cv2.imwrite(main_path + "threshold.png", pic)
	# Character recognition with tesseract
	final = pytesseract.image_to_string(Image.open(main_path + "threshold.png"))
	return final

# string1 = get_string(main_path)
# print(string1)
# print("\n\n\n")
print(pytesseract.image_to_string(Image.open("plate_344.jpg")))

string2 = pytesseract.image_to_string(Image.open("plate_344.jpg"))
print(string2)
string2 = re.sub(r"\. |[^\w\.\* ]| \.| (?=/)", "", string2)
string2 = list(string2.split(" "))
print(string2)

# string2 = pytesseract.image_to_string(Image.open("LICENSE_PLATE.PNG"))
# if any(state in string2 for state in state_names):
#     print(string2)

# print("\n\n\n")
# print(string2)