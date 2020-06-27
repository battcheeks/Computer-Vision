
import cv2
import numpy as np
from time import sleep

video = cv2.VideoCapture(1)
#video.set(cv2.CAP_PROP_FPS, 1)

while True:
    ret, orig_frame = video.read()
    if not ret:
        video = cv2.VideoCapture("road_car_view.mp4")
        continue

    frame = cv2.GaussianBlur(orig_frame, (5, 5), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    low_red = np.array([160, 100, 100])
    up_red = np.array([180, 255, 255])
    low_green=np.array([36,100,100])
    up_green=np.array([70,255,255])
    low_black=np.array([0,0,0])
    up_black=np.array([180,150,50])
    mask1 = cv2.inRange(hsv, low_black, up_black)
    mask2 = cv2.inRange(hsv, low_green, up_green)
    mask = cv2.inRange(hsv, low_red, up_red)
    edges = cv2.Canny(mask, 250, 255)
    edges1 = cv2.Canny(mask1, 250, 255)
    edges2 = cv2.Canny(mask2, 250, 255)
    #contours, hierarchy =cv2.findContours(edges,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #cv2.drawContours(frame, contours, 0, (0, 255, 0), 3) 
    lines = cv2.HoughLinesP(edges, 2, np.pi/180, 150, maxLineGap=20)
    #lines1 = cv2.HoughLinesP(edges1, 2, np.pi/180, 150, maxLineGap=100)
    #lines2 = cv2.HoughLinesP(edges2, 2, np.pi/180, 150, maxLineGap=100)
    if lines is not None:
       for line in lines:
          x1, y1, x2, y2 = line[0]
          cv2.line(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
    #if lines1 is not None:
     #  for line1 in lines1:
      #    x1,y1,x2,y2=line1[0]
       #   cv2.line(frame,(x1,y1),(x2,y2),(255,0,0),5)
    #if lines2 is not None:
     #  for line2 in lines2:
      #    x1,y1,x2,y2=line2[0]
       #   cv2.line(frame,(x1,y1),(x2,y2),(0,255,0),5)
    cv2.imshow("edges", edges)
    cv2.imshow("frame", frame)
    #cv2.imshow("con",con)
    sleep(0.05)
    
   

    key = cv2.waitKey(1)
    if key == 27:
       break
video.release()
cv2.destroyAllWindows()
