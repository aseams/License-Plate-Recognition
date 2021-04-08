"""TestLPR.py"""
# Params for Pre-Processing
# PARAMS TESTED {13, 0}, {11,2}, {19,0}
ADAPTIVE_THRESH_BLOCK_SIZE = 13
ADAPTIVE_THRESH_WEIGHT = 0

# Params for Plate Detection
SML_CTR_MIN_RATIO = 0.01			# 0.01
SML_CTR_MAX_RATIO = 0.8			 	# 0.8
PLATE_MAX_ASPECT_RATIO = 8			# 8
CTR_MIN_EXTENT_RATIO = 0.75			# 0.75

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

API_KEY = "2b9aae527888957"

