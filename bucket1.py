'''plan of aciton is to threshold only red and blue color and mask it on a frame and then use contours
to detect the rectangle shaped buckets and depending on the number of buckets calculate their midpoint'''
import cv2
import numpy as np
cap=cv2.VideoCapture(0)
if cap.isOpened():
    while(True):
        ret, frame=cap.read()
        frame_gau=cv2.GaussianBlur(frame,(3,3),0)
        hsv=cv2.cvtColor(frame_gau,cv2.COLOR_BGR2HSV)
        lred=np.array([136,87,111],np.uint8)
        hred=np.array([179,255,255],np.uint8)
        lblue=np.array([99,115,150],np.uint8)
        hblue=np.array([110,255,255],np.uint8)
        red=cv2.inRange(hsv,lred,hred)
        blue=cv2.inRange(hsv,lblue,hblue)
        kernal=np.ones((5,5),"uint8")
        red = cv2.dilate(red, kernal)
        res = cv2.bitwise_and(frame_gau, frame_gau, mask=red)
        blue = cv2.dilate(blue, kernal)
        res1 = cv2.bitwise_and(frame_gau,frame_gau, mask=blue)
        contours, hierarchy = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        red_array=[]
        blue_array=[]
        for pic,contour in enumerate(contours):
            area1=cv2.contourArea(contour)
            if(area1>700):
                x,y,w,h=cv2.boundingRect(contour)
                if(w>=1.5*h and w<=2*h):
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),4)
                    M=cv2.moments(contour)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
                a=str(x+(w/2))
                red_array.append(a)
        contours, hierarchy = cv2.findContours(blue, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for pic,contour in enumerate(contours):
            area1=cv2.contourArea(contour)
            if(area1>700):
                x,y,w,h=cv2.boundingRect(contour)
                if(w>=1.5*h and w<=2*h):
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),4)
                    M=cv2.moments(contour)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
                b=str(x+(w/2))
                blue_array.append(b)
        #canny_red=cv2.Canny(red_gray,250,255)
        cv2.namedWindow('canny', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('canny',600,600)
        cv2.imshow('canny', frame)
        if(len(red_array)>0 or len(blue_array)>0):
            print(red_array+blue_array)
        '''cv2.namedWindow('red_gray', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('red_gray', 600, 600)
        cv2.imshow('red_gray', fin_gray)'''
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()
else:
    print('no cam')
