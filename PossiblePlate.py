import cv2
import numpy as np

"""
Holds all variables for each possible plate
"""
class PossiblePlate:

	# constructor #################################################################################
	def __init__(self):
		self.imgPlate = None
		self.imgGrayscale = None
		self.imgThresh = None

		self.rrLocationOfPlateInScene = None

		self.strChars = ""