from multipledispatch import dispatch

@dispatch(str,str)
def writeToFile(filepath, filename):
	cv2.imwrite(filepath, filename)

