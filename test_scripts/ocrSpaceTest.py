# import requests
# import json
# import constants

# overlay = True
# api_key = constants.API_KEY
# language = "eng"
# filename = "../standard.jpg"
# OCREngine = 2

# def ocr_space_file(filename, overlay, api_key, language, OCREngine):
# 	""" OCR.space API request with local file.
# 		Python3.5 - not tested on 2.7
# 	:param filename: Your file path & name.
# 	:param overlay: Is OCR.space overlay required in your response.
# 					Defaults to False.
# 	:param api_key: OCR.space API key.
# 					Defaults to 'helloworld'.
# 	:param language: Language code to be used in OCR.
# 					List of available language codes can be found on https://ocr.space/OCRAPI
# 					Defaults to 'en'.
# 	:return: Result in JSON format.
# 	"""

# 	payload = {'isOverlayRequired': overlay,
# 			   'apikey': api_key,
# 			   'language': language,
# 			   'OCREngine': OCREngine
# 			   }
# 	with open(filename, 'rb') as f:
# 		r = requests.post('https://api.ocr.space/parse/image',
# 						  files={filename: f},
# 						  data=payload,
# 						  )
# 		r.raw.decode_content = True
# 		f.write(r.content)
# 	return r.content.decode()

# test_file = ocr_space_file(filename, overlay, api_key, language, OCREngine)

# print(test_file)




import ocrspace
import requests


api = ocrspace.API()
TEST_IMAGE_URL = 'https://user-images.githubusercontent.com/19779081/45311273-38cb8400-b546-11e8-9cb0-a660bf07806e.png'

print('Testing URL-based OCR:')
print(api.ocr_url(TEST_IMAGE_URL))

print('Testing file-based OCR:')
# Download image for demo purposes
TEST_FILENAME = '1.png'
with open(TEST_FILENAME, 'wb') as f:
    r = requests.get(TEST_IMAGE_URL)
    r.raw.decode_content = True
    f.write(r.content)

# With file path
print(api.ocr_file(TEST_FILENAME))
# With file pointer
print(api.ocr_file(open(TEST_FILENAME, 'rb')))