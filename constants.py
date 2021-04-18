"""colors for use with LPR_Final.py"""
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

"""constants for preprocessing.py"""
GAUSSIAN_SMOOTH_FILTER_SIZE = (5, 5)
ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 9

"""constants for findPlates.py"""
PLATE_WIDTH_PADDING_FACTOR = 1.3
PLATE_HEIGHT_PADDING_FACTOR = 1.5

"""constants for use with checkIfPossibleChar, this checks one possible char only (does not compare to another char)"""
MIN_PIXEL_WIDTH = 2
MIN_PIXEL_HEIGHT = 8

MIN_ASPECT_RATIO = 0.25
MAX_ASPECT_RATIO = 1.0

MIN_PIXEL_AREA = 80

"""constants for comparing two chars"""
MIN_DIAG_SIZE_MULTIPLE_AWAY = 0.3
MAX_DIAG_SIZE_MULTIPLE_AWAY = 5.0

MAX_CHANGE_IN_AREA = 0.5

MAX_CHANGE_IN_WIDTH = 0.8
MAX_CHANGE_IN_HEIGHT = 0.2

MAX_ANGLE_BETWEEN_CHARS = 12.0

"""other constants"""
MIN_NUMBER_OF_MATCHING_CHARS = 3

RESIZED_CHAR_IMAGE_WIDTH = 20
RESIZED_CHAR_IMAGE_HEIGHT = 30

MIN_CONTOUR_AREA = 100


"""characterRecognition"""
typeface = 'Typeface.png'
plate = 'plate_344.jpg'
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

"""Assigned at start of LPR_Final.py"""
API_KEY = ""