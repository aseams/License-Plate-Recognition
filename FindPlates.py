import cv2
import numpy as np
import math
import LPR_Final
import random

import preprocess
import FindChars
import PossiblePlate
import PossibleChar
import constants

###################################################################################################
def detectPlatesInScene(originalImage):
	"""
	Finds all possible plates in image by looking for rectangle contours
	"""
	plateList = []                   # this will be the return value

	height, width, numChannels = originalImage.shape

	imgGrayscale = np.zeros((height, width, 1), np.uint8)
	imgThresh = np.zeros((height, width, 1), np.uint8)
	imgContours = np.zeros((height, width, 3), np.uint8)

	cv2.destroyAllWindows()

	if LPR_Final.showSteps == True: # show steps #######################################################
		cv2.imshow("0", originalImage)
		cv2.imwrite("./LPR_Output/FindPlate_0.png", originalImage)
	# end if # show steps #########################################################################

	imgGrayscale, imgThresh = preprocess.preprocess(originalImage)         # preprocess to get grayscale and threshold images

	if LPR_Final.showSteps == True: # show steps #######################################################
		cv2.imshow("1a", imgGrayscale)
		cv2.imshow("1b", imgThresh)

		cv2.imwrite("./LPR_Output/FindPlate_1a.png", imgGrayscale)
		cv2.imwrite("./LPR_Output/FindPlate_1b.png", imgThresh)
	# end if # show steps #########################################################################

			# find all possible chars in the scene,
			# this function first finds all contours, then only includes contours that could be chars (without comparison to other chars yet)
	possibleCharList = findPossibleCharsInScene(imgThresh)

	if LPR_Final.showSteps == True: # show steps #######################################################
		print("step 2 - len(possibleCharList) = " + str(
			len(possibleCharList)))  # 131 with MCLRNF1 image

		imgContours = np.zeros((height, width, 3), np.uint8)

		contours = []

		for possibleChar in possibleCharList:
			contours.append(possibleChar.contour)
		# end for

		cv2.drawContours(imgContours, contours, -1, constants.SCALAR_WHITE)
		cv2.imshow("2b", imgContours)
		cv2.imwrite("./LPR_Output/FindPlate_2b.png", imgContours)
	# end if # show steps #########################################################################

			# given a list of all possible chars, find groups of matching chars
			# in the next steps each group of matching chars will attempt to be recognized as a plate
	allPossibleStrings = FindChars.findListOfListsOfMatchingChars(possibleCharList)

	if LPR_Final.showSteps == True: # show steps #######################################################
		print("step 3 - allPossibleStrings.Count = " + str(
			len(allPossibleStrings)))  # 13 with MCLRNF1 image

		imgContours = np.zeros((height, width, 3), np.uint8)

		for matchingChars in allPossibleStrings:
			intRandomBlue = random.randint(0, 255)
			intRandomGreen = random.randint(0, 255)
			intRandomRed = random.randint(0, 255)

			contours = []

			for matchingChar in matchingChars:
				contours.append(matchingChar.contour)
			# end for

			cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
		# end for

		cv2.imshow("3", imgContours)
		cv2.imwrite("./LPR_Output/FindPlate_3.png", imgContours)
	# end if # show steps #########################################################################

	for matchingChars in allPossibleStrings:                   # for each group of matching chars
		possiblePlate = extractPlate(originalImage, matchingChars)         # attempt to extract plate

		if possiblePlate.imgPlate is not None:                          # if plate was found
			plateList.append(possiblePlate)                  # add to list of possible plates
		# end if
	# end for

	print("\n" + str(len(plateList)) + " possible plates found")  # 13 with MCLRNF1 image

	if LPR_Final.showSteps == True: # show steps #######################################################
		print("\n")
		cv2.imshow("4a", imgContours)
		cv2.imwrite("./LPR_Output/FindPlate_4a.png", imgContours)

		for i in range(0, len(plateList)):
			p2fRectPoints = cv2.boxPoints(plateList[i].rrLocationOfPlateInScene)

			cv2.line(imgContours, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), constants.SCALAR_RED, 2)
			cv2.line(imgContours, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), constants.SCALAR_RED, 2)
			cv2.line(imgContours, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), constants.SCALAR_RED, 2)
			cv2.line(imgContours, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), constants.SCALAR_RED, 2)

			cv2.imshow("4a", imgContours)
############cv2.imwrite("FindPlate_4a.png", imgContours)

			print("possible plate " + str(i) + ", click on any image and press a key to continue . . .")

			cv2.imshow("4b", plateList[i].imgPlate)
			cv2.imwrite("./LPR_Output/FindPlate_4b.png", plateList[i].imgPlate)
			cv2.waitKey(0)
		# end for

		print("\nplate detection complete, click on any image and press a key to begin char recognition . . .\n")
		cv2.waitKey(0)
	# end if # show steps #########################################################################

	return plateList
# end function

###################################################################################################
def findPossibleCharsInScene(imgThresh):
	"""
	Similar to detectPlatesInScene(originalImage) except that it looks for characters in each rectangle.
	"""
	listOfPossibleChars = []                # this will be the return value

	intCountOfPossibleChars = 0

	imgThreshCopy = imgThresh.copy()

	contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)   # find all contours

	height, width = imgThresh.shape
	imgContours = np.zeros((height, width, 3), np.uint8)

	for i in range(0, len(contours)):                       # for each contour

		if LPR_Final.showSteps == True: # show steps ###################################################
			cv2.drawContours(imgContours, contours, i, constants.SCALAR_WHITE)
		# end if # show steps #####################################################################

		possibleChar = PossibleChar.PossibleChar(contours[i])

		if FindChars.checkIfPossibleChar(possibleChar):                   # if contour is a possible char, note this does not compare to other chars (yet) . . .
			intCountOfPossibleChars = intCountOfPossibleChars + 1           # increment count of possible chars
			listOfPossibleChars.append(possibleChar)                        # and add to list of possible chars
		# end if
	# end for

	if LPR_Final.showSteps == True: # show steps #######################################################
		print("\nstep 2 - len(contours) = " + str(len(contours)))  # 2362 with MCLRNF1 image
		print("step 2 - intCountOfPossibleChars = " + str(intCountOfPossibleChars))  # 131 with MCLRNF1 image
		cv2.imshow("2a", imgContours)
		cv2.imwrite("./LPR_Output/FindPlate_2a.png", imgContours)
	# end if # show steps #########################################################################

	return listOfPossibleChars
# end function


###################################################################################################
def extractPlate(imgOriginal, matchingChars):
	"""
	Extract plate image using contours/bounding box
	"""
	possiblePlate = PossiblePlate.PossiblePlate()           # this will be the return value

	matchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)        # sort chars from left to right based on x position

			# calculate the center point of the plate
	fltPlateCenterX = (matchingChars[0].intCenterX + matchingChars[len(matchingChars) - 1].intCenterX) / 2.0
	fltPlateCenterY = (matchingChars[0].intCenterY + matchingChars[len(matchingChars) - 1].intCenterY) / 2.0

	ptPlateCenter = fltPlateCenterX, fltPlateCenterY

			# calculate plate width and height
	intPlateWidth = int((matchingChars[len(matchingChars) - 1].intBoundingRectX + matchingChars[len(matchingChars) - 1].intBoundingRectWidth - matchingChars[0].intBoundingRectX) * constants.PLATE_WIDTH_PADDING_FACTOR)

	intTotalOfCharHeights = 0

	for matchingChar in matchingChars:
		intTotalOfCharHeights = intTotalOfCharHeights + matchingChar.intBoundingRectHeight
	# end for

	fltAverageCharHeight = intTotalOfCharHeights / len(matchingChars)

	intPlateHeight = int(fltAverageCharHeight * constants.PLATE_HEIGHT_PADDING_FACTOR)

			# calculate correction angle of plate region
	fltOpposite = matchingChars[len(matchingChars) - 1].intCenterY - matchingChars[0].intCenterY
	fltHypotenuse = FindChars.distanceBetweenChars(matchingChars[0], matchingChars[len(matchingChars) - 1])
	fltCorrectionAngleInRad = math.asin(fltOpposite / fltHypotenuse)
	fltCorrectionAngleInDeg = fltCorrectionAngleInRad * (180.0 / math.pi)

			# pack plate region center point, width and height, and correction angle into rotated rect member variable of plate
	possiblePlate.rrLocationOfPlateInScene = ( tuple(ptPlateCenter), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg )

			# final steps are to perform the actual rotation

			# get the rotation matrix for our calculated correction angle
	rotationMatrix = cv2.getRotationMatrix2D(tuple(ptPlateCenter), fltCorrectionAngleInDeg, 1.0)

	height, width, numChannels = imgOriginal.shape      # unpack original image width and height

	rotatedImage = cv2.warpAffine(imgOriginal, rotationMatrix, (width, height))       # rotate the entire image

	croppedImage = cv2.getRectSubPix(rotatedImage, (intPlateWidth, intPlateHeight), tuple(ptPlateCenter))

	possiblePlate.imgPlate = croppedImage         # copy the cropped plate image into the applicable member variable of the possible plate

	return possiblePlate
# end function