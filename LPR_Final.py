import cv2
import numpy as np
from tkinter import filedialog
from tkinter import *

import os
from pathlib import Path
import sys

import FindChars
import FindPlates
import PossiblePlate
import constants
import doubleCheck

showSteps = False
###################################################################################################

def main():
	"""
	Main function. Calls other functions/files. 
	"""
	blnKNNTrainingSuccessful = FindChars.loadKNNDataAndTrainKNN()         # attempt KNN training

	if blnKNNTrainingSuccessful == False:                               # if KNN training was not successful
		print("\nerror: KNN traning was not successful\n")  # show error message
		return                                                          # and exit program
	# end if
	doubleCheck.ensure_dir("./LPR_Output")
	with open("API_KEY.txt", "r") as file:
    	constants.API_KEY = file.read()

	root = Tk()
	root.withdraw()
	selected_folder = filedialog.askdirectory()
	print('\nSelected: ' + selected_folder + "\n")
	extensions = ['.jpg', '.png', '.jpeg']
	images = [x for x in Path(selected_folder).iterdir() if x.suffix.lower() in extensions]
	for img in images:
		head, tail = os.path.split(str(img))
		#originalImage = cv2.imread("LicPlateImages/" + tail)
		# if originalImage is None:                            # if image was not read successfully
		# print(str(img))
		# print('head: ' + head)
		# print('tail: ' + tail)
		originalImage = cv2.imread(str(img))
		if originalImage is None:                            # if image was not read successfully
			print("\nerror: image not read from file \n\n")  # print error message to std out
			os.system("pause")                                  # pause so user can see error message
			return                                              # and exit program
		# end if

		plateList = FindPlates.detectPlatesInScene(originalImage)           # detect plates

		plateList = FindChars.detectCharsInPlates(plateList)        # detect chars in plates

		cv2.imshow("originalImage", originalImage)            # show scene image
		#cv2.imwrite("./LPR_Output/originalImage.png", originalImage)

		if len(plateList) == 0:                          # if no plates were found
			print("\nno license plates were detected\n")  # inform user no plates were found
		else:
			# if we get in here list of possible plates has at leat one plate

			# sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
			plateList.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)

			# suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
			truePlate = plateList[0]

			cv2.imshow("imgPlate", truePlate.imgPlate)           # show crop of plate and threshold of plate
			cv2.imshow("imgThresh", truePlate.imgThresh)
			#cv2.imwrite("./LPR_Output/imgPlate.png", truePlate.imgPlate)           # show crop of plate and threshold of plate
			#cv2.imwrite("./LPR_Output/imgThresh.png", truePlate.imgThresh)

			if len(truePlate.strChars) == 0:                     # if no chars were found in the plate
				print("\nno characters were detected\n\n")  # show message
				return                                          # and exit program
		# end if

			drawRedRectangleAroundPlate(originalImage, truePlate)             # draw red rectangle around plate

			print("----------------------------------------")
			print("\nlicense plate read from image = " + truePlate.strChars + "\n")  # write license plate text to std out

			writeLicensePlateCharsOnImage(originalImage, truePlate)           # write license plate text on the image

			cv2.imshow("originalImage", originalImage)                # re-show scene image
			outputFilename = (truePlate.strChars.lower() + ".png")
			outputPath = ("./LPR_Output/" + outputFilename)
			cv2.imwrite(outputPath, originalImage)           # write image out to file

		# end if else

		#cv2.waitKey(0)					# hold windows open until user presses a key
		doubleCheck.confirmDB(truePlate.strChars.lower())

	database.close()
	return

###################################################################################################
def drawRedRectangleAroundPlate(originalImage, truePlate):
	"""
	Draws a rectangle around the found plate. Uses tuples of points to make each side of the rectangle.
	"""

	p2fRectPoints = cv2.boxPoints(truePlate.rrLocationOfPlateInScene)            # get 4 vertices of rotated rect

	cv2.line(originalImage, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), constants.SCALAR_RED, 2)         # draw 4 red lines
	cv2.line(originalImage, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), constants.SCALAR_RED, 2)
	cv2.line(originalImage, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), constants.SCALAR_RED, 2)
	cv2.line(originalImage, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), constants.SCALAR_RED, 2)

###################################################################################################
def writeLicensePlateCharsOnImage(originalImage, truePlate):
	"""
	Writes characters on top of input image. Also includes rectangle around plate.
	"""
	CenterTextAreaX = 0                             # this will be the center of the area the text will be written to
	CenterTextAreaY = 0

	BottomLeftTextBoxX = 0                          # this will be the bottom left of the area that the text will be written to
	BottomLeftTextBoxY = 0

	sceneHeight, sceneWidth, sceneNumChannels = originalImage.shape
	plateHeight, plateWidth, plateNumChannels = truePlate.imgPlate.shape

	intFontFace = cv2.FONT_HERSHEY_SIMPLEX                      # choose a plain jane font
	fltFontScale = float(plateHeight) / 30.0                    # base font scale on height of plate area
	intFontThickness = int(round(fltFontScale * 1.5))           # base font thickness on font scale

	textSize, baseline = cv2.getTextSize(truePlate.strChars, intFontFace, fltFontScale, intFontThickness)        # call getTextSize

			# unpack roatated rect into center point, width and height, and angle
	( (intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg ) = truePlate.rrLocationOfPlateInScene

	intPlateCenterX = int(intPlateCenterX)              # make sure center is an integer
	intPlateCenterY = int(intPlateCenterY)

	CenterTextAreaX = int(intPlateCenterX)         # the horizontal location of the text area is the same as the plate

	if intPlateCenterY < (sceneHeight * 0.75):                                                  # if the license plate is in the upper 3/4 of the image
		CenterTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))      # write the chars in below the plate
	else:                                                                                       # else if the license plate is in the lower 1/4 of the image
		CenterTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))      # write the chars in above the plate
	# end if

	textSizeWidth, textSizeHeight = textSize                # unpack text size width and height

	BottomLeftTextBoxX = int(CenterTextAreaX - (textSizeWidth / 2))           # calculate the lower left origin of the text area
	BottomLeftTextBoxY = int(CenterTextAreaY + (textSizeHeight / 2))          # based on the text area center, width, and height

			# write the text on the image
	cv2.putText(originalImage, truePlate.strChars, (BottomLeftTextBoxX, BottomLeftTextBoxY), intFontFace, fltFontScale, constants.SCALAR_YELLOW, intFontThickness)

###################################################################################################
if __name__ == "__main__":
	main()