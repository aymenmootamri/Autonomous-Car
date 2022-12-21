import numpy as np
import cv2 as cv


def thresholding(img):
    imghsv=cv.cvtColor(img,cv.COLOR_BGR2HSV)
    lowerwhite=np.array([80,0,0])
    upperwhite=np.array([179,160,255])
    maskwhite=cv.inRange(imghsv,lowerwhite,upperwhite)
    #this will give us the color that we desire that we have mentionned in the 2 previous lines
    return maskwhite



def warpImg(img,points,w,h,inv=False):
    pts1=np.float32(points)
    pts2=np.float32([[0,0],[w,0],[0,h],[w,h]])
    if inv:
        matrix=cv.getPerspectiveTransform(pts2,pts1)
    else:
        matrix=cv.getPerspectiveTransform(pts1,pts2)
    
    imgWarp=cv.warpPerspective(img,matrix,(w,h))
    return imgWarp

def nothing():
    pass
def initializeTrackbars(initialTracbarVals,wT=480, ht=240):
    cv.namedWindow("Trackbars")
    cv.resizeWindow("Trackbars",360,240)
    cv.createTrackbar("Width Top","Trackbars",initialTracbarVals[0],wT//2,nothing)
    cv.createTrackbar("Height Top","Trackbars",initialTracbarVals[1],ht,nothing)
    cv.createTrackbar("Width Bottom","Trackbars",initialTracbarVals[2],wT//2,nothing)
    cv.createTrackbar("Height Bottom","Trackbars",initialTracbarVals[3],ht,nothing)

def valTrackbars(wT=480,hT=240):
    widthTop=cv.getTrackbarPos("Width Top","Trackbars")
    heightTop=cv.getTrackbarPos("Height Top","Trackbars")
    widthBottom=cv.getTrackbarPos("Width Bottom","Trackbars")
    heightBottom=cv.getTrackbarPos("Height Bottom","Trackbars")
    points=np.float32([(widthTop,heightTop),(wT-widthTop,heightTop),
    (widthBottom,heightBottom),(wT-widthBottom,heightBottom)])
    return points
def drawPoints(img,points):
    for x in range(4):
        cv.circle(img,(int(points[x][0]),int(points[x][1])),15,(0,0,255),cv.FILLED)
    return img


### STEP 3
def getHistogram(img,minPerc=0.1,display=False,region=1):
    if region==1:
        histValues=np.sum(img,axis=0)
    else:
        histValues=np.sum(img[img.shape[0]//region:,:],axis=0)
    #print(histValues)
    maxValue=np.max(histValues)
    #print(maxValue)
    minValue=minPerc*maxValue
    
    indexArray=np.where(histValues >=minValue)
    #print(indexArray)
    basePoint=int(np.average(indexArray))
    #print(basePoint)
    if display:
        imgHist=np.zeros((img.shape[0],img.shape[1],3),np.uint8)
        for x,intensity in enumerate(histValues):
            cv.line(imgHist,(x,img.shape[0]),(x,img.shape[0]-intensity//255//region),(255,0,255),2)
            cv.circle(imgHist,(basePoint,img.shape[0]),20,(0,255,255),cv.FILLED)
        return basePoint,imgHist
    return basePoint     
   


def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv.cvtColor(imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver