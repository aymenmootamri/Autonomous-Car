import cv2 as cv
import numpy as np
import utlis


curveList=list()
avgVal=10


def getLaneCurve(img,display=2):
    imgCopy=img.copy()
    imgResult=img.copy()
    
    ####STEP1
    imgthres=utlis.thresholding(img)
    

    ####STEP2
    hT,wT,c=img.shape
    points=utlis.valTrackbars()
    imgWarp=utlis.warpImg(imgthres,points,wT,hT)
    imgPoints=utlis.drawPoints(imgCopy,points)
   

    ###STEP3

    middlePoint,imgHist=utlis.getHistogram(imgWarp,minPerc=0.5,display=True,region=4)
    CurveAveragePoint,imgHist=utlis.getHistogram(imgWarp,minPerc=0.9,display=True)
    CurveRaw=CurveAveragePoint-middlePoint

    ###STEP4
    curveList.append(CurveRaw)
    if(len(curveList)>avgVal):
        curveList.pop(0)
    curve=int(sum(curveList)/len(curveList))

    ### STEP5
    if display != 0:
        imgInvWarp = utlis.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv.cvtColor(imgInvWarp, cv.COLOR_GRAY2BGR)
        imgInvWarp[0:hT // 3, 0:wT] = 0, 0, 0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv.addWeighted(imgResult, 1, imgLaneColor, 1, 0)
        midY = 450
        cv.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT // 20
            cv.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
        #fps = cv.getTickFrequency() / (cv2.getTickCount() - timer);
        #cv.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3);
    if display == 2:
        imgStacked = utlis.stackImages(0.7, ([img, imgPoints, imgWarp],
                                             [imgHist, imgLaneColor, imgResult]))
        cv.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv.imshow('Resutlt', imgResult)

    ###NORMALISATION
    """the curve value is ranging between -60 to 60, something like that, we need to do normalisation: We will change it from -1 to 1"""
    curve=curve/100
    if curve>=1:curve=1
    if curve <=-1:curve=-1
    return curve



if __name__ == '__main__':
    cap=cv.VideoCapture("test.mp4")
    initialTracbarVals=[102,80,20,214]
    utlis.initializeTrackbars(initialTracbarVals)
    frameCounter=0
    while True:
        frameCounter+=1
        if cap.get(cv.CAP_PROP_FRAME_COUNT)==frameCounter:
            cap.set(cv.CAP_PROP_POS_FRAMES,0)
            frameCounter=0
        success,img=cap.read()
        img_resized=cv.resize(img,(480,240))
        curve=getLaneCurve(img_resized,display=2)
        print(curve)
        
        if cv.waitKey(10)& 0xFF==ord('d'):
            break
    cap.release()
    cv.destroyAllWindows()