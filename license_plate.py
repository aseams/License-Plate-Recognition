import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import PIL

#reading in the input image
plate = cv2.imread("D:/andys/Documents/Kean University/4 Spring 2021/Senior Project/ProjCode/_premade image tests/input_images/1.png")

#function that shows the image
def display(img, cmap = 'gray'):
    fig = plt.figure(figsize = (12,10))
    ax = fig.add_subplot(111)
    ax.imshow(img,cmap = 'gray')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite("D:/andys/Documents/Kean University/4 Spring 2021/Senior Project/ProjCode/RESTART/_EXAMPLE_INPUTS/UPDATE_1.png",img)

#need to change color of picture from BGR to RGB
plate = cv2.cvtColor(plate, cv2.COLOR_BGR2RGB)
display(plate)

#Cascade Classifier where our hundres of samples of license plates are
plate_cascade = cv2.CascadeClassifier('C:/Users/andys/AppData/Local/Programs/Python/Python38-32/Lib/site-packages/cv2/data/haarcascade_number_plate.xml')


def detect_plate(img):
    
    plate_img = plate.copy()
    
    #gets the points of where the classifier detects a plate
    plate_rects = plate_cascade.detectMultiScale(plate_img, scaleFactor = 1.2, minNeighbors = 10)

    #draws the rectangle around it
    for (x,y,w,h) in plate_rects:
        cv2.rectangle(plate_img, (x,y), (x+w, y+h), (255,0,0), 5)

    return plate_img

#detects the plate and zooms in on it
def detect_zoom_plate(img, kernel):
    
    plate_img = img.copy()
    
    #gets the points of where the classifier detects a plate
    plate_rects = plate_cascade.detectMultiScale(plate_img, scaleFactor = 1.2, minNeighbors = 10) #maxSize = (100,100))
    
    for (x,y,w,h) in plate_rects:
        x_offset = x
        y_offset = y
        
        x_end = x+w
        y_end = y+h
        
        #getting the points that show the license plate
        zoom_img = plate_img[y_offset:y_end, x_offset:x_end]
        #increasing the size of the image
        zoom_img = cv2.resize(zoom_img, (0,0),fx = 2, fy = 2)
        zoom_img = zoom_img[7:-7, 7:-7]
        #sharpening the image to make it look clearer
        zoom_img = cv2.filter2D(zoom_img, -1, kernel)
        
        zy = (40 - (y_end - y_offset))//2
        zx = (144 - (x_end-x_offset))//2
        
        ydim = (y_end+zy-50) - (y_offset-zy-50)
        xdim = (x_end+zx) - (x_offset-zx)
       
       
        zoom_img = cv2.resize(zoom_img,(xdim,ydim))
        
        #putting the zoomed in image above where the license plate is located
        try:
            plate_img[y_offset-zy-55:y_end+zy-55, x_offset-zx:x_end+zx] = zoom_img
        except:
            pass
         
        #drawing a rectangle
        for (x,y,w,h) in plate_rects:
            cv2.rectangle(plate_img, (x,y), (x+w, y+h), (255,0,0), 2)
            
        
    return plate_img

#same function as above just blurs the license plate instead
def detect_blur(img):
    
    plate_img = img.copy()
    
    
    plate_rects = plate_cascade.detectMultiScale(plate_img, scaleFactor = 1.2, minNeighbors = 3)
    
    for (x,y,w,h) in plate_rects:
        x_offset = x
        y_offset = y
        
        x_end = x+w
        y_end = y+h
        
        zoom_img = plate_img[y_offset:y_end, x_offset:x_end]
        #blur function
        zoom_img = cv2.medianBlur(zoom_img,15)
        plate_img[y_offset:y_end, x_offset:x_end] = zoom_img
        
        for (x,y,w,h) in plate_rects:
            cv2.rectangle(plate_img, (x,y), (x+w, y+h), (255,0,0), 5)
        
    return plate_img

def find_plate_rectangle(img):
    # print('find_plate_rectangle()')
    # This function finds plate in the image.
    # The idea is to find a rectangle within the image

    contours, method = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)

    contours = [c for c in contours
                if cv2.contourArea(c) > img.size * SML_CTR_MIN_RATIO
                and cv2.contourArea(c) < img.size * SML_CTR_MAX_RATIO]
    ret = []
    for c in contours:
        peri = cv2.arcLength(c, True)
        ## 0.02 is epsilon
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            area = cv2.contourArea(c)
            rect_area = w * h
            extent = float(area) / rect_area
            aspect_ratio = float(w) / h
            if extent > CTR_MIN_EXTENT_RATIO and aspect_ratio < PLATE_MAX_ASPECT_RATIO:
                ret.append(approx)
    return ret

#matrix needed to sharpen the image
kernel = np.array([[-1,-1,-1],
                   [-1,9,-1],
                   [-1,-1,-1]])

result = find_plate_rectangle(plate)
result = cv2.rectangle(plate, (x, y), (x + w, y + h), (0, 255, 0), 2)
display(result)

# result = detect_zoom_plate(plate, kernel)
# display(result)

# result = detect_blur(plate)
# display(result)
