import cv2 as cv
cap=cv.VideoCapture(0)
def getImg(display=False):
    isTrue,img=cap.read()
    img=cv.resize(img,(480,240))
    if display:
        cv.imshow("vid",img)


    return img

if __name__=="__main__":
    while True:
        img=getImg(True)
        if cv.waitKey(20) & 0xFF ==ord('d'):
            break
    cap.release()
    cv.destroyAllWindows()
