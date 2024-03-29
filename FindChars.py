import os

import cv2
import numpy as np
import math
import random

import LPR_Final
import preprocess
import PossibleChar
import constants

kNearest = cv2.ml.KNearest_create()

def loadKNNDataAndTrainKNN():
	"""
	Loads and runs KNN training to ensure best results
	"""
	allContoursWithData = []                # declare empty lists,
	validContoursWithData = []              # we will fill these shortly

	try:
		npaClassifiers = np.loadtxt("classifications.txt", np.float32)                  # read in training classifications
	except:                                                                             # if file could not be opened
		print("error, unable to open classifications.txt, exiting program\n")  			# show error message
		os.system("pause")
		return False                                                                    # and return False
	# end try

	try:
		npaFlatImages = np.loadtxt("flattened_images.txt", np.float32)                 # read in training images
	except:                                                                            # if file could not be opened
		print("error, unable to open flattened_images.txt, exiting program\n")  	   # show error message
		os.system("pause")
		return False                                                                   # and return False
	# end try

	npaClassifiers = npaClassifiers.reshape((npaClassifiers.size, 1))       		   # reshape numpy array to 1d, necessary to pass to call to train
	kNearest.setDefaultK(1)                                                 		   # set default K to 1
	kNearest.train(npaFlatImages, cv2.ml.ROW_SAMPLE, npaClassifiers)           		   # train KNN object

	return True                             # if we got here training was successful so return true
# end function

def detectCharsInPlates(plateList):
	"""
	Used to detect any possible characters within the image. Then throws out characters not found inside of a rectangle.
	"""
	intPlateCounter = 0
	imgContours = None
	contours = []

	if len(plateList) == 0:          # if list of possible plates is empty
		return plateList             # return
	# end if

			# at this point we can be sure the list of possible plates has at least one plate

	for possiblePlate in plateList:          # for each possible plate, this is a big for loop that takes up most of the function

		possiblePlate.imgGrayscale, possiblePlate.imgThresh = preprocess.preprocess(possiblePlate.imgPlate)     # preprocess to get grayscale and threshold images

		if LPR_Final.showSteps == True: # show steps
			cv2.imshow("5a", possiblePlate.imgPlate)
			cv2.imshow("5b", possiblePlate.imgGrayscale)
			cv2.imshow("5c", possiblePlate.imgThresh)

			cv2.imwrite("./LPR_Output/FindChars_5a.png", possiblePlate.imgPlate)
			cv2.imwrite("./LPR_Output/FindChars_5b.png", possiblePlate.imgGrayscale)
			cv2.imwrite("./LPR_Output/FindChars_5c.png", possiblePlate.imgThresh)
		# end if # show steps

				# increase size of plate image for easier viewing and char detection
		possiblePlate.imgThresh = cv2.resize(possiblePlate.imgThresh, (0, 0), fx = 1.6, fy = 1.6)

				# threshold again to eliminate any gray areas
		thresholdValue, possiblePlate.imgThresh = cv2.threshold(possiblePlate.imgThresh, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

		if LPR_Final.showSteps == True: # show steps
			cv2.imshow("5d", possiblePlate.imgThresh)
			cv2.imwrite("./LPR_Output/FindChars_5d.png", possiblePlate.imgThresh)
		# end if # show steps

				# find all possible chars in the plate,
				# this function first finds all contours, then only includes contours that could be chars (without comparison to other chars yet)
		listOfPossibleCharsInPlate = findPossibleCharsInPlate(possiblePlate.imgGrayscale, possiblePlate.imgThresh)

		if LPR_Final.showSteps == True: # show steps
			height, width, numChannels = possiblePlate.imgPlate.shape
			imgContours = np.zeros((height, width, 3), np.uint8)
			del contours[:]                                         # clear the contours list

			for possibleChar in listOfPossibleCharsInPlate:
				contours.append(possibleChar.contour)
			# end for

			cv2.drawContours(imgContours, contours, -1, constants.SCALAR_WHITE)

			cv2.imshow("6", imgContours)
			cv2.imwrite("./LPR_Output/FindChars_6.png", imgContours)
		# end if # show steps

				# given a list of all possible chars, find groups of matching chars within the plate
		listOfListsOfMatchingCharsInPlate = findListOfListsOfMatchingChars(listOfPossibleCharsInPlate)

		if LPR_Final.showSteps == True: # show steps
			imgContours = np.zeros((height, width, 3), np.uint8)
			del contours[:]

			for matchingChars in listOfListsOfMatchingCharsInPlate:
				intRandomBlue = random.randint(0, 255)
				intRandomGreen = random.randint(0, 255)
				intRandomRed = random.randint(0, 255)

				for matchingChar in matchingChars:
					contours.append(matchingChar.contour)
				# end for
				cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
			# end for
			cv2.imshow("7", imgContours)
			cv2.imwrite("./LPR_Output/FindChars_7.png", imgContours)
		# end if # show steps #

		if (len(listOfListsOfMatchingCharsInPlate) == 0):			# if no groups of matching chars were found in the plate

			if LPR_Final.showSteps == True: # show steps #
				print("chars found in plate number " + str(
					intPlateCounter) + " = (none), click on any image and press a key to continue . . .")
				intPlateCounter = intPlateCounter + 1
				cv2.destroyWindow("8")
				cv2.destroyWindow("9")
				cv2.destroyWindow("10")
				cv2.waitKey(0)
			# end if # show steps #

			possiblePlate.strChars = ""
			continue						# go back to top of for loop
		# end if

		for i in range(0, len(listOfListsOfMatchingCharsInPlate)):                              # within each list of matching chars
			listOfListsOfMatchingCharsInPlate[i].sort(key = lambda matchingChar: matchingChar.intCenterX)        # sort chars from left to right
			listOfListsOfMatchingCharsInPlate[i] = removeInnerOverlappingChars(listOfListsOfMatchingCharsInPlate[i])              # and remove inner overlapping chars
		# end for

		if LPR_Final.showSteps == True: # show steps #
			imgContours = np.zeros((height, width, 3), np.uint8)

			for matchingChars in listOfListsOfMatchingCharsInPlate:
				intRandomBlue = random.randint(0, 255)
				intRandomGreen = random.randint(0, 255)
				intRandomRed = random.randint(0, 255)

				del contours[:]

				for matchingChar in matchingChars:
					contours.append(matchingChar.contour)
				# end for

				cv2.drawContours(imgContours, contours, -1, (intRandomBlue, intRandomGreen, intRandomRed))
			# end for
			cv2.imshow("8", imgContours)
			cv2.imwrite("./LPR_Output/FindChars_8.png", imgContours)
		# end if # show steps #

				# within each possible plate, suppose the longest list of potential matching chars is the actual list of chars
		intLenOfLongestListOfChars = 0
		intIndexOfLongestListOfChars = 0

				# loop through all the vectors of matching chars, get the index of the one with the most chars
		for i in range(0, len(listOfListsOfMatchingCharsInPlate)):
			if len(listOfListsOfMatchingCharsInPlate[i]) > intLenOfLongestListOfChars:
				intLenOfLongestListOfChars = len(listOfListsOfMatchingCharsInPlate[i])
				intIndexOfLongestListOfChars = i
			# end if
		# end for

				# suppose that the longest list of matching chars within the plate is the actual list of chars
		longestListOfMatchingCharsInPlate = listOfListsOfMatchingCharsInPlate[intIndexOfLongestListOfChars]

		if LPR_Final.showSteps == True: # show steps #
			imgContours = np.zeros((height, width, 3), np.uint8)
			del contours[:]

			for matchingChar in longestListOfMatchingCharsInPlate:
				contours.append(matchingChar.contour)
			# end for

			cv2.drawContours(imgContours, contours, -1, constants.SCALAR_WHITE)

			cv2.imshow("9", imgContours)
			cv2.imwrite("./LPR_Output/FindChars_9.png", imgContours)
		# end if # show steps #

		possiblePlate.strChars = recognizeCharsInPlate(possiblePlate.imgThresh, longestListOfMatchingCharsInPlate)

		if LPR_Final.showSteps == True: # show steps #
			print("chars found in plate number " + str(
				intPlateCounter) + " = " + possiblePlate.strChars + ", click on any image and press a key to continue . . .")
			intPlateCounter = intPlateCounter + 1
			cv2.waitKey(0)
		# end if # show steps #

	# end of big for loop that takes up most of the function

	if LPR_Final.showSteps == True:
		print("\nchar detection complete, click on any image and press a key to continue . . .\n")
		cv2.waitKey(0)
	# end if

	return plateList
# end function

def findPossibleCharsInPlate(imgGrayscale, imgThresh):
	"""
	Locates all possible characters
	"""
	listOfPossibleChars = []                        # this will be the return value
	contours = []
	imgThreshCopy = imgThresh.copy()

			# find all contours in plate
	contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

	for contour in contours:                        # for each contour
		possibleChar = PossibleChar.PossibleChar(contour)

		if checkIfPossibleChar(possibleChar):              # if contour is a possible char, note this does not compare to other chars (yet) . . .
			listOfPossibleChars.append(possibleChar)       # add to list of possible chars
		# end if
	# end if

	return listOfPossibleChars
# end function

def checkIfPossibleChar(possibleChar):
	"""
	Confirms whether a specific contour might be a character.
	"""
	if (possibleChar.intBoundingRectArea > constants.MIN_PIXEL_AREA and
		possibleChar.intBoundingRectWidth > constants.MIN_PIXEL_WIDTH and possibleChar.intBoundingRectHeight > constants.MIN_PIXEL_HEIGHT and
		constants.MIN_ASPECT_RATIO < possibleChar.fltAspectRatio and possibleChar.fltAspectRatio < constants.MAX_ASPECT_RATIO):
		return True
	else:
		return False
	# end if
# end function

def findListOfListsOfMatchingChars(listOfPossibleChars):
	"""
	Using all possible chars in one list, rearrange the chars into a list of lists containing matching char strings.
	"""
	listOfListsOfMatchingChars = []                  # this will be the return value

	for possibleChar in listOfPossibleChars:                        # for each possible char in the one big list of chars
		matchingChars = findListOfMatchingChars(possibleChar, listOfPossibleChars)        # find all chars in the big list that match the current char

		matchingChars.append(possibleChar)                # also add the current char to current possible list of matching chars

		if len(matchingChars) < constants.MIN_NUMBER_OF_MATCHING_CHARS:     # if current possible list of matching chars is not long enough to constitute a possible plate
			continue                            # jump back to the top of the for loop and try again with next char, note that it's not necessary
												# to save the list in any way since it did not have enough chars to be a possible plate
		# end if

												# if we get here, the current list passed test as a "group" or "cluster" of matching chars
		listOfListsOfMatchingChars.append(matchingChars)      # so add to our list of lists of matching chars

		listOfPossibleCharsWithCurrentMatchesRemoved = []

												# remove the current list of matching chars from the big list so we don't use those same chars twice,
												# make sure to make a new big list for this since we don't want to change the original big list
		listOfPossibleCharsWithCurrentMatchesRemoved = list(set(listOfPossibleChars) - set(matchingChars))

		recursiveListOfListsOfMatchingChars = findListOfListsOfMatchingChars(listOfPossibleCharsWithCurrentMatchesRemoved)      # recursive call

		for recursiveListOfMatchingChars in recursiveListOfListsOfMatchingChars:        # for each list of matching chars found by recursive call
			listOfListsOfMatchingChars.append(recursiveListOfMatchingChars)             # add to our original list of lists of matching chars
		# end for

		break       # exit for

	# end for

	return listOfListsOfMatchingChars
# end function

def findListOfMatchingChars(possibleChar, listOfChars):
	"""
	Given a possible character and a list of possible characters, find all chars in main list that match, and return a list of matches.
	"""
	matchingChars = []                # this will be the return value

	for possibleMatchingChar in listOfChars:                # for each char in big list
		if possibleMatchingChar == possibleChar:    # if the char we attempting to find matches for is the exact same char as the char in the big list we are currently checking
													# then we should not include it in the list of matches b/c that would end up double including the current char
			continue                                # so do not add to list of matches and jump back to top of for loop
		# end if
					# compute stuff to see if chars are a match
		fltDistanceBetweenChars = distanceBetweenChars(possibleChar, possibleMatchingChar)

		fltAngleBetweenChars = angleBetweenChars(possibleChar, possibleMatchingChar)

		fltChangeInArea = float(abs(possibleMatchingChar.intBoundingRectArea - possibleChar.intBoundingRectArea)) / float(possibleChar.intBoundingRectArea)

		fltChangeInWidth = float(abs(possibleMatchingChar.intBoundingRectWidth - possibleChar.intBoundingRectWidth)) / float(possibleChar.intBoundingRectWidth)
		fltChangeInHeight = float(abs(possibleMatchingChar.intBoundingRectHeight - possibleChar.intBoundingRectHeight)) / float(possibleChar.intBoundingRectHeight)

				# check if chars match
		if (fltDistanceBetweenChars < (possibleChar.fltDiagonalSize * constants.MAX_DIAG_SIZE_MULTIPLE_AWAY) and
			fltAngleBetweenChars < constants.MAX_ANGLE_BETWEEN_CHARS and
			fltChangeInArea < constants.MAX_CHANGE_IN_AREA and
			fltChangeInWidth < constants.MAX_CHANGE_IN_WIDTH and
			fltChangeInHeight < constants.MAX_CHANGE_IN_HEIGHT):

			matchingChars.append(possibleMatchingChar)        # if the chars are a match, add the current char to list of matching chars
		# end if
	# end for

	return matchingChars                  # return result
# end function

def distanceBetweenChars(firstChar, secondChar):
	"""
	Use Pythagorean theorem to calculate distance between two chars
	"""
	intX = abs(firstChar.intCenterX - secondChar.intCenterX)
	intY = abs(firstChar.intCenterY - secondChar.intCenterY)

	return math.sqrt((intX ** 2) + (intY ** 2))
# end function

def angleBetweenChars(firstChar, secondChar):
	"""
	Use basic trigonometry (SOH CAH TOA) to calculate angle between chars
	"""
	fltAdj = float(abs(firstChar.intCenterX - secondChar.intCenterX))
	fltOpp = float(abs(firstChar.intCenterY - secondChar.intCenterY))

	if fltAdj != 0.0:                           # check to make sure we do not divide by zero if the center X positions are equal, float division by zero will cause a crash in Python
		fltAngleInRad = math.atan(fltOpp / fltAdj)      # if adjacent is not zero, calculate angle
	else:
		fltAngleInRad = 1.5708                          # if adjacent is zero, use this as the angle, this is to be consistent with the C++ version of this program
	# end if

	fltAngleInDeg = fltAngleInRad * (180.0 / math.pi)       # calculate angle in degrees

	return fltAngleInDeg
# end function

def removeInnerOverlappingChars(matchingChars):
	"""
	If multiple chars overlap, remove the inner char. Prevents including same char twice if multiple contours are found for the same physical char.
	Ex: 'O' has an outer 'O' and an inner 'o'
	'R' has an outer 'R' and an inner 'D' 
	"""
	listOfMatchingCharsWithInnerCharRemoved = list(matchingChars)                # this will be the return value

	for currentChar in matchingChars:
		for otherChar in matchingChars:
			if currentChar != otherChar:        # if current char and other char are not the same char . . .
																			# if current char and other char have center points at almost the same location . . .
				if distanceBetweenChars(currentChar, otherChar) < (currentChar.fltDiagonalSize * constants.MIN_DIAG_SIZE_MULTIPLE_AWAY):
								# if we get in here we have found overlapping chars
								# next we identify which char is smaller, then if that char was not already removed on a previous pass, remove it
					if currentChar.intBoundingRectArea < otherChar.intBoundingRectArea:         # if current char is smaller than other char
						if currentChar in listOfMatchingCharsWithInnerCharRemoved:              # if current char was not already removed on a previous pass . . .
							listOfMatchingCharsWithInnerCharRemoved.remove(currentChar)         # then remove current char
						# end if
					else:                                                                       # else if other char is smaller than current char
						if otherChar in listOfMatchingCharsWithInnerCharRemoved:                # if other char was not already removed on a previous pass . . .
							listOfMatchingCharsWithInnerCharRemoved.remove(otherChar)           # then remove other char
						# end if
					# end if
				# end if
			# end if
		# end for
	# end for

	return listOfMatchingCharsWithInnerCharRemoved
# end function

def recognizeCharsInPlate(imgThresh, matchingChars):
	"""
	Applies true character recognition
	"""
	strChars = ""               # this will be the return value, the chars in the lic plate

	height, width = imgThresh.shape

	imgThreshColor = np.zeros((height, width, 3), np.uint8)

	matchingChars.sort(key = lambda matchingChar: matchingChar.intCenterX)        # sort chars from left to right

	cv2.cvtColor(imgThresh, cv2.COLOR_GRAY2BGR, imgThreshColor)                     # make color version of threshold image so we can draw contours in color on it

	for currentChar in matchingChars:                                         # for each char in plate
		pt1 = (currentChar.intBoundingRectX, currentChar.intBoundingRectY)
		pt2 = ((currentChar.intBoundingRectX + currentChar.intBoundingRectWidth), (currentChar.intBoundingRectY + currentChar.intBoundingRectHeight))

		cv2.rectangle(imgThreshColor, pt1, pt2, constants.SCALAR_GREEN, 2)           # draw green box around the char

				# crop char out of threshold image
		imgROI = imgThresh[currentChar.intBoundingRectY : currentChar.intBoundingRectY + currentChar.intBoundingRectHeight,
						   currentChar.intBoundingRectX : currentChar.intBoundingRectX + currentChar.intBoundingRectWidth]

		imgROIResized = cv2.resize(imgROI, (constants.RESIZED_CHAR_IMAGE_WIDTH, constants.RESIZED_CHAR_IMAGE_HEIGHT))           # resize image, this is necessary for char recognition

		npaROIResized = imgROIResized.reshape((1, constants.RESIZED_CHAR_IMAGE_WIDTH * constants.RESIZED_CHAR_IMAGE_HEIGHT))        # flatten image into 1d numpy array

		npaROIResized = np.float32(npaROIResized)               # convert from 1d numpy array of ints to 1d numpy array of floats

		retval, npaResults, neigh_resp, dists = kNearest.findNearest(npaROIResized, k = 1)              # finally we can call findNearest !!!

		strCurrentChar = str(chr(int(npaResults[0][0])))            # get character from results

		strChars = strChars + strCurrentChar                        # append current char to full string

	# end for

	if LPR_Final.showSteps == True: # show steps #
		cv2.imshow("10", imgThreshColor)
		cv2.imwrite("./LPR_Output/FindChars_10.png", imgThreshColor)
	# end if # show steps #

	return strChars
# end function