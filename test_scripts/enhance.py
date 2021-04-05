import cv2
from cv2 import dnn_superres
import glob
import sys
import os

sr = dnn_superres.DnnSuperResImpl_create()
# Read the desired model
path = "LapSRN_x4.pb"
sr.readModel(path)

# Set the desired model and scale to get correct pre- and post-processing
sr.setModel("lapsrn", 4)

input_location = input("Input File: ")
#input_location = "D:/andys/Documents/Kean University/4 Spring 2021/Senior Project/ProjCode/RESTART/cropped_vehicle"
#for img in glob.glob("{0}/*.jpg".format(input_location)):
	# Upscale the image
image = cv2.imread(input_location)
#image = cv2.imread(img)
cv2.waitKey(500)
result = sr.upsample(image)
filename = input_location
#path, filename = os.path.split(img)
print("upscaled " + filename)
cv2.destroyWindow("ORIG")
cv2.waitKey(500)
# Save the image
#cv2.imwrite("cropped_vehicle/upscaled/" + str(filename), result)
cv2.imwrite("upscaled_" + str(filename), result)
print("wrote " + filename + " to file")