import cv2
import numpy as np
import math

class PossibleChar:
	"""
	:self.contour: Holds the contour for each char in scene
	:self.boundingRect: Holds the bounding rectangle points for each char in scene
	:self.intBoundingRectX: Used for distanceBetweenChars() = abs(firstChar.intCenterX - secondChar.intCenterX)
	:self.intBoundingRectY: Used for distanceBetweenChars() = abs(firstChar.intCenterY - secondChar.intCenterY)
	:self.intBoundingRectWidth: Width of possible character. Used in conjunction with intBoundingRectX to get X position
	:self.intBoundingRectHeight: Height of possible character. Used in conjunction with intBoundingRectY to get Y position
	:self.intBoundingRectArea: Area of possible char
	:self.intCenterX: Used mainly for distance and angle between chars
	:self.intCenterY: Used mainly for distance and angle between chars
	:self.fltDiagonalSize: Used to find matching chars
	:self.fltAspectRatio: Used to check if rectangle contains possible char
	"""
	def __init__(self, _contour):
		self.contour = _contour

		self.boundingRect = cv2.boundingRect(self.contour)

		[intX, intY, intWidth, intHeight] = self.boundingRect

		self.intBoundingRectX = intX
		self.intBoundingRectY = intY
		self.intBoundingRectWidth = intWidth
		self.intBoundingRectHeight = intHeight

		self.intBoundingRectArea = self.intBoundingRectWidth * self.intBoundingRectHeight

		self.intCenterX = (self.intBoundingRectX + self.intBoundingRectX + self.intBoundingRectWidth) / 2
		self.intCenterY = (self.intBoundingRectY + self.intBoundingRectY + self.intBoundingRectHeight) / 2

		self.fltDiagonalSize = math.sqrt((self.intBoundingRectWidth ** 2) + (self.intBoundingRectHeight ** 2))

		self.fltAspectRatio = float(self.intBoundingRectWidth) / float(self.intBoundingRectHeight)