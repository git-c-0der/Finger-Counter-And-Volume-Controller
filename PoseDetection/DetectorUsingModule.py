import cv2
import PoseModule as pm
import time

cap = cv2.VideoCapture('PoseVideos/Vid1.mp4')

ptime = 0
detector = pm.poseDetector()
while True:
    ret, img = cap.read()
    img = cv2.resize(img, (640, 480))

    img = detector.findPose(img)
    lmList = detector.findPosition(img, False)
    # print(lmList)

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, str(int(fps)), (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 154, 200), 3)
    cv2.imshow('Video1', img)

    # cv2.waitKey(1)
    if cv2.waitKey(10) == ord('q'):
        break