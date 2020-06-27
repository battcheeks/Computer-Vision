from imutils.video import VideoStream
import cv2
#cap=cv2.VideoCapture(0)
cam = VideoStream(src=0).start()
while True:
    frame = cam.read()
    #ret,frame1=cap.read()
    if frame is not None:# and frame1 is not None:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('frame',gray)
        #cv2.imshow('frame1',gray1)
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # thresh=cv2.convertScaleAbs(thresh)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # mode: cv2.RETR_EXTERNAL, cv2.RETR_LIST, cv2.RETR_TREE
        # method: cv2.CHAIN_APPROX_SIMPLE, cv2.CHAIN_APPROX_TC89_L1, cv2.CHAIN_APPROX_TC89_KCOS
        for pic, contour in enumerate(contours):
            area1 = cv2.contourArea(contour)
            if (area1 > 700):
                x, y, w, h = cv2.boundingRect(contour)
                if (w * 1.5 < h):
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 165, 255), 2)
                    M = cv2.moments(contour)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
        # cnt = contours[0]
        # x,y,w,h = cv2.boundingRect(cnt)
        # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        # rect = cv2.minAreaRect(cnt)
        # box = cv2.boxPoints(rect)
        # box = np.int0(box)
        # cv2.drawContours(img,[box],0,(0,255,0),2)
        cv2.imshow('Original', frame)
        #cv2.imshow('Gray', gray)
        #cv2.imshow('Thresh', thresh)

    # Display the resulting frame

    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()
cam.stop()