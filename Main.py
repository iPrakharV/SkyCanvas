from splitter import Splitter
import cv2
camera = cv2.VideoCapture("videos/demo1.mp4")

splitter = Splitter()

while True:
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    points = splitter.split_points(gray)
    for i in points:
        print(i)
        cv2.circle(frame,(int(i[0][0]),int(i[0][1])),4,(0,0,255),-1)
        
    


    cv2.imshow("window",frame)
    cv2.waitKey(1)

