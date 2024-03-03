### Compatible with Python 2.7
### OpenCV (2.4)
### Numpy (1.26.4)

import cv2
import numpy as np

if cv2.imread('Foto.png') is not None:
        img = cv2.imread('Foto.png')
elif  cv2.imread('Foto.jpg') is not None:
        img = cv2.imread('Foto.jpg')

#Default image values
scale_percent = 60
invert_image = 0

###----Controlls----###
def nothing(x):
	pass
    
cv2.namedWindow("Controls",cv2.WINDOW_NORMAL)

cv2.createTrackbar("Scale","Controls",50,100,nothing)
cv2.createTrackbar("Brightness", "Controls",255, 2*255,nothing)
cv2.createTrackbar("Contrast","Controls",127, 2*127,nothing) 
cv2.createTrackbar("Sigma_low","Controls",0,4,nothing)
cv2.createTrackbar("Sigma_high","Controls",0,4,nothing)
cv2.createTrackbar("Erosion","Controls",0,10,nothing)
cv2.createTrackbar("Opening","Controls",0,10,nothing)
cv2.createTrackbar("Area_min","Controls",0,2000,nothing)
cv2.createTrackbar("Blur","Controls",0,4,nothing)
cv2.createTrackbar("Invert","Controls",0,1,nothing)


def controller(img, brightness=255, contrast=127):
    brightness = int((brightness-0)*(255-(-255))/(510-0)+(-255))
    contrast = int((contrast-0)*(127-(-127))/(254-0)+(-127))
  
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            max = 255
        else:
            shadow = 0
            max = 255 + brightness
  
        al_pha = (max-shadow)/255
        ga_mma = shadow

        cal = cv2.addWeighted(img, al_pha,img, 0, ga_mma)
  
    else:
        cal = img
  
    if contrast != 0:
        Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        Gamma = 127 * (1 - Alpha)

        cal = cv2.addWeighted(cal, Alpha,cal, 0, Gamma)
  
    return cal

while(True):
    cv2.imshow("Original",img)
    
    ###----Scale the image----###
    scale_percent=cv2.getTrackbarPos("Escala","Controls")+1
    
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
  
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    
    cv2.imshow("Original",resized)
    
    ###----Contrast and brightness----###
    brightness = cv2.getTrackbarPos("Brightness","Controls")
    contrast = cv2.getTrackbarPos("Contrast","Controls")
                                  
      
    effect = controller(resized,brightness,contrast)
                        
    gray = cv2.cvtColor(effect, cv2.COLOR_BGR2GRAY)
    
    ###----Difference of Gaussians----###
    sigma_low=3+2*((cv2.getTrackbarPos("Sigma_low","Controls")))
    sigma_high=5+2*((cv2.getTrackbarPos("Sigma_high","Controls")))
    
    if(sigma_high>sigma_low):
        low_sigma = cv2.GaussianBlur(gray,(sigma_low,sigma_low),0)
        high_sigma = cv2.GaussianBlur(gray,(sigma_high,sigma_high),0)
    else:
        low_sigma = cv2.GaussianBlur(gray,(3,3),0)
        high_sigma = cv2.GaussianBlur(gray,(5,5),0)

    DoG = low_sigma - high_sigma
    
    ###----Openings----###
    opening=cv2.getTrackbarPos("Opening","Controls")+1
    kernel = np.ones((opening,opening),np.uint8)
    
    open_img = cv2.morphologyEx(DoG, cv2.MORPH_CLOSE, kernel)
    
    ###---Line erosion---###
    ersosión=cv2.getTrackbarPos("Erosion","Controls")+1
    kernel = np.ones((ersosión, ersosión), np.uint8)
    DoG_Erode = cv2.erode(open_img, kernel)
    
    ###---Noise cleaning---###

    area_min=cv2.getTrackbarPos("Area_min","Controls")+1
    thresh = cv2.threshold(DoG_Erode, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    
    cnts = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        area = cv2.contourArea(c)
        if area < area_min:
            cv2.drawContours(thresh, [c], -1, (255,255,255), -1)
    
    ###---Smooth image---###
    blur=1+(2*cv2.getTrackbarPos("Blur","Controls"))
    
    blur_img = cv2.medianBlur(thresh,blur)

    if cv2.getTrackbarPos("Invert","Controls")==1:
            blur_img = (255-blur_img)
            
    cv2.imshow('Invert_Img',blur_img)
    
    ###---Save Image---###
    if cv2.waitKey(1) & 0xFF == 27:
        width = int(img.shape[1] * 300 / 100)
        height = int(img.shape[0] * 300 / 100)
        dim = (width, height)
  
        final = cv2.resize(blur_img, dim, interpolation = cv2.INTER_AREA)
        
        cv2.imwrite("Final_Image.jpg",final)
        print("Done")
        break
    
