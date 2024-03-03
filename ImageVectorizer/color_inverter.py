### Compatible with Python 2.7
### OpenCV (2.4)
### Numpy (1.26.4)

import cv2
import numpy as np

if cv2.imread('Inv.png') is not None:
        img = cv2.imread('Inv.png')
elif  cv2.imread('Inv.jpg') is not None:
        img = cv2.imread('Inv.jpg')

scale_factor = 0.35

def nothing(x):
	pass

while(True):
    cv2.imshow("Original",img)
    
    ###----Scale the image----###
    width = int(img.shape[1] * scale_factor)
    height = int(img.shape[0] * scale_factor)
    dim = (width, height)
  
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    cv2.imshow("Original",resized)
    invert_img = (255-resized)
            
    cv2.imshow('Invert_Img',invert_img)
    cv2.imwrite("Final_Image.jpg",invert_img)
    
    ###---Save Image---###
    print("Done")
    cv2.destroyWindow("Invert_Img")
    cv2.destroyWindow("Original")
    break

        
        
        
    
    
