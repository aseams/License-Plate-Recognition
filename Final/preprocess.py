import cv2
import numpy as np
import math
import constants

###################################################################################################
def preprocess(imgOriginal):
	imgGrayscale = extractValue(imgOriginal)

	imgMaxContrastGrayscale = maximizeContrast(imgGrayscale)

	height, width = imgGrayscale.shape

	imgBlurred = np.zeros((height, width, 1), np.uint8)

	imgBlurred = cv2.GaussianBlur(imgMaxContrastGrayscale, constants.GAUSSIAN_SMOOTH_FILTER_SIZE, 0)

	imgThresh = cv2.adaptiveThreshold(imgBlurred, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, constants.ADAPTIVE_THRESH_BLOCK_SIZE, constants.ADAPTIVE_THRESH_WEIGHT)

	return imgGrayscale, imgThresh

###################################################################################################
def extractValue(imgOriginal):
	height, width, numChannels = imgOriginal.shape

	imgHSV = np.zeros((height, width, 3), np.uint8)

	imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

	imgHue, imgSaturation, imgValue = cv2.split(imgHSV)

	return imgValue

###################################################################################################
def maximizeContrast(imgGrayscale):

	height, width = imgGrayscale.shape

	imgTopHat = np.zeros((height, width, 1), np.uint8)
	imgBlackHat = np.zeros((height, width, 1), np.uint8)

	structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

	imgTopHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_TOPHAT, structuringElement)
	imgBlackHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_BLACKHAT, structuringElement)

	imgGrayscalePlusTopHat = cv2.add(imgGrayscale, imgTopHat)
	imgGrayscalePlusTopHatMinusBlackHat = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

	return imgGrayscalePlusTopHatMinusBlackHat