import cv2
import json
import numpy as np

# path 
path = 'D:/andys/Documents/Kean University/4 Spring 2021/Senior Project/ProjCode/RESTART/_EXAMPLE_INPUTS/20210325_113555.jpg'
plate_cascade = cv2.CascadeClassifier('C:/Users/andys/AppData/Local/Programs/Python/Python38-32/Lib/site-packages/cv2/data/haarcascade_number_plate.xml')
   
# Reading an image in default mode
image = cv2.imread(path,0)

print('Original Dimensions : ',image.shape)
 
scale_percent = 60 # percent of original size
width = int(image.shape[1] * scale_percent / 100)
height = int(image.shape[0] * scale_percent / 100)
dim = (width, height)
resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)

def detect_plate(img):
    
    plate_img = image.copy()
    
    #gets the points of where the classifier detects a plate
    plate_rects = plate_cascade.detectMultiScale(plate_img, scaleFactor = 1.08, minNeighbors = 15)

    #draws the rectangle around it
    for (x,y,w,h) in plate_rects:
        cv2.rectangle(plate_img, (x,y), (x+w, y+h), (255,0,0), 5)

    return plate_img

ret = detect_plate(resized)

cv2.imshow("generated", ret)
startX = 273 * scale_percent/100
startY = 974 * scale_percent/100
endX = 515 * scale_percent/100
endY = 2260 * scale_percent/100

start_point = (584,163)
end_point = (1356,309)
color = [255,0,0]
thickness = 20

print(image)
print(start_point)
print(end_point)
print(color)
print(thickness)

# resize image
resized2 = cv2.rectangle(img=resized, pt1=start_point, pt2=end_point, color=color, lineType=thickness)

print('Resized Dimensions : ',resized.shape)
 
cv2.imshow("Resized image", resized)
  
# Displaying the image 
# cv2.imshow(window_name, image)
cv2.waitKey(0)