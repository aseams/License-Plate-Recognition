import os
import sys
import json
import requests
import re

import constants
import database

def ensure_dir(file_path):
	directory = os.path.realpath(file_path)
	if not os.path.exists(directory):
		print('Creating directory: ' + os.path.basename(directory))
		os.makedirs(directory)

def confirmDB(origPlate):
	yes = {"yes": True, "y": True, "ye": True}
	no = {"no": False, "n": False}
	retry = ["r", "retry", "re", "try"]
	prompt = " [y/n/retry] "
	
	while True:
		print("Add " + origPlate + " to database? " + prompt)
		choice = input().lower()

		if choice in yes:
			comment = input("Please type any comments now. If you do not want to add a comment, simply press [ENTER].") or ""
			database.insert(origPlate, comment)
			break
		elif choice in no:
			break
		elif choice in retry:
			print("Retrying OCR...")
			file = ("./LPR_Output/" + origPlate + ".png")
			state, plate = getOCR(file)
		else:
			print("Please respond with 'yes', 'no', or 'retry'\
										('y', 'n', or 'r').\n")

def getOCR(filename):
	"""
	OCR.space API request with local file.
	:param filename: Your file path & name.
	:param overlay: Is OCR.space overlay required in your response.
					Defaults to False.
	:param api_key: OCR.space API key.
					Defaults to 'helloworld'.
	:param language: Language code to be used in OCR.
					List of available language codes can be found on https://ocr.space/OCRAPI
					Defaults to 'en'.
	:return: Result in JSON format.
	"""
	overlay = False
	api_key = constants.API_KEY
	language = 'eng'
	OCREngine = 2
	print("Sent to API")
	payload = {'isOverlayRequired': overlay,
			   'apikey': api_key,
			   'language': language,
			   'OCREngine': OCREngine
			   }
	with open(filename, 'rb') as f:
		r = requests.post('https://api.ocr.space/parse/image',
						  files={filename: f},
						  data=payload,
						  )
	print("Received API response")
	# jason = json.dumps(r.json(),indent = 2, sort_keys = True)
	# jason = json.loads(jason)
	jason = r.json()
	#print('jason\n' + jason)
	#print('jason\n\n' + jason + '\n\n')
	print(type(jason))
	print(json.dumps(r.json(), indent = 4))
	parsedText = jason['ParsedResults'][0]['ParsedText']
	print('Parsed Text:\n' + parsedText)
	top = jason['ParsedResults'][0]['ParsedText']
	middle = jason['ParsedResults'][0]['ParsedText']
	print(type(parsedText))
	state, plate = decodeJSON(parsedText)
	return state,plate

def decodeJSON(jason):
	jason = re.split('[\n,.=}]',jason)
	print('ocr_text_split: ' + str(jason))
	#jason = [word for word in jason if len(word) in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]]
	#print('ocr_text_len: ' + str(jason))
	# if " " in jason[0]:
	# 	state = jason[0].strip()
	# else:
	# 	state = jason[0]

	# if " " in jason[1]:
	# 	plate = jason[1].strip()
	# else:
	# 	plate = jason[1]
	# print('ocr_text_final: ' + str(jason))
	state = stateExists(jason)
	if state == "error":
		print("\nState not found/confirmed")
	for i in jason:
		if len(i) in [5,6,7]:
			plate = i
	print('state ' + state)
	print('plate: ' + plate)
	return state, plate
	# if confirmDB(state, plate):
	# 	print("Adding " + state + ":" + plate + " to database")
	# else:
	# 	print("Skipped adding " + state + ":" + plate + " to database.")
	# print("Plate is: {0}".format(jason.split("\n")[4]))
	# print("Plate is: {}".format(jason.split("; |, |\n")[4]))


	#print("Full Text:\n" + json_dict['ParsedResults'][0]['ParsedText'])
	#print("Top Line: " + json_dict['ParsedResults'][0]['TextOverlay']['Lines'][0]['LineText'])
	#print("Middle Line: " + json_dict['ParsedResults'][0]['TextOverlay']['Lines'][1]['LineText'])
	#print("Bottom Line: " + json_dict['ParsedResults'][0]['TextOverlay']['Lines'][2]['LineText'])

def stateExists(state):
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

	common_issues = {"":"Alaska", "":"Alabama", "":"Arkansas", "":"American Samoa", 
				   "":"Arizona", "IN Cn bijouvia":"California", "":"Colorado", "":"Connecticut", 
				   "":"District of Columbia", "":"Delaware", "":"Florida", 
				   "":"Georgia", "":"Guam", "":"Hawaii", "":"Iowa", "":"Idaho", 
				   "":"Illinois", "":"Indiana", "":"Kansas", "":"Kentucky", 
				   "":"Louisiana", "":"Massachusetts", "":"Maryland", "":"Maine", 
				   "":"Michigan", "":"Minnesota", "":"Missouri", "":"Mississippi", 
				   "":"Montana", "":"North Carolina", "":"North Dakota", 
				   "":"Nebraska", "":"New Hampshire", "Garden State":"New Jersey", 
				   "":"New Mexico", "":"Nevada", "":"New York", "":"Ohio", 
				   "":"Oklahoma", "":"Oregon", "":"Pennsylvania", "":"Puerto Rico", 
				   "":"Rhode Island", "":"South Carolina", "":"South Dakota", 
				   "":"Tennessee", "":"Texas", "":"Utah", "":"Virginia", 
				   "":"Virgin Islands", "":"Vermont", "":"Washington", "":"Wisconsin", 
				   "":"West Virginia", "":"Wyoming"}

	state_abrv  = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE",
				   "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", 
				   "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", 
				   "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", 
				   "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", 
				   "VT", "VA", "WA", "WV", "WI", "WY"]

	for i in state:
		i = i.capitalize()
		if i in state_names:
			return i
		elif i in state_abrv:
			idx = state_names.index(i)
			return str(state_names[idx])
		elif i in common_issues.values():
			return str(common_issues.get(i))
		else:
			return "error"