import cv2 as cv
import numpy as np


cv.namedWindow("HSV")
cv.resizeWindow("HSV",640,240)

def empty():
    pass
cv.createTrackbar("HUE min","HSV",0,179,empty)
cv.createTrackbar("HUE max","HSV",179,179,empty)
cv.createTrackbar("Sat min","HSV",0,255,empty)
cv.createTrackbar("Sat max","HSV",255,255,empty)
cv.createTrackbar("Val min","HSV",0,255,empty)
cv.createTrackbar("Val max","HSV",255,255,empty)
vid=cv.VideoCapture("test.mp4")
frameCounter=0

while True:
    #this is used to still repeating the video
    frameCounter+=1
    if vid.get(cv.CAP_PROP_FRAME_COUNT)==frameCounter:
        vid.set(cv.CAP_PROP_POS_FRAMES,0)
        frameCounter=0
    isTrue,img=vid.read()
    img=cv.resize(img,(480,240))
    imghsv=cv.cvtColor(img,cv.COLOR_BGR2HSV)

    h_min=cv.getTrackbarPos("HUE min","HSV")
    h_max=cv.getTrackbarPos("HUE max","HSV")
    s_min=cv.getTrackbarPos("Sat min","HSV")
    s_max=cv.getTrackbarPos("Sat max","HSV")
    v_min=cv.getTrackbarPos("Val min","HSV")
    v_max=cv.getTrackbarPos("Val max","HSV")
    lower_color=np.array([h_min,s_min,v_min])
    upper_color=np.array([h_max,s_max,v_max])
    mask_color=cv.inRange(imghsv,lower_color,upper_color)
    mask_color_bgr=cv.cvtColor(mask_color,cv.COLOR_GRAY2BGR) 
  #We did this because mask_color is 1 channel and img and result are 3 channel ,and is hstack we should put variables with the same number of channels,that's why
    result=cv.bitwise_and(img,img,mask=mask_color)
    horizontalstack=np.hstack([img,mask_color_bgr,result])
    #cv.imshow("video_bgr",img)
    #cv.imshow("video_hsv",mask_color)
    #cv.imshow("result",result)
    cv.imshow("Horizontal Stacking",horizontalstack)
    if (cv.waitKey(20) & 0xFF==ord('d')):
        break