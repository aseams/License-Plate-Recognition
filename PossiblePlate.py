import cv2
import numpy as np

class PossiblePlate:
	"""
	:self.imgPlate: original image
	:self.imgGrayscale: grayscale image
	:self.imgThresh: thresholded image
	:self.rrLocationOfPlateInScene: rectangle location in scene
	:self.strChars: plate value found
	"""
	def __init__(self):
		self.imgPlate = None
		self.imgGrayscale = None
		self.imgThresh = None
		self.rrLocationOfPlateInScene = None
		self.strChars = ""