import os
import HandTrackingModule as htm
import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(1)

folderPath = 'Finger Images'
myList = os.listdir(folderPath)
imgList = []
for imgPath in myList:
    image = cv2.imread(f'{folderPath}/{imgPath}')
    image = cv2.resize(image, (200, 200))
    imgList.append(image)

detector = htm.handDetector()
tipIds = [4, 8, 12, 16, 20]
ptime = 0
while True:
    ret, img = cap.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (800, 600))

    img = detector.findHands(img)
    lmList = detector.findPositions(img, draw=False)

    if len(lmList) > 0:
        fingers = []
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totalFingers = fingers.count(1)

        img[0:200, 0:200] = imgList[totalFingers - 1]

        cv2.rectangle(img, (20, 355), (170, 525), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (43, 475), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, f'FPS: {int(fps)}', (610, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 10, 55), 3)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imshow('Image', img)
    if cv2.waitKey(30) == ord('q'):
        break
