import cv2
import time
import numpy as np
import HandTrackingModule as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

###############################################
wcam, hcam = 640, 480
###############################################

cap = cv2.VideoCapture(1)
cap.set(3, wcam)
cap.set(4, hcam)
ptime = 0

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volumerange = volume.GetVolumeRange()
minvol = volumerange[0]
maxvol = volumerange[1]
vol, volBar, volPer = 0, 400, 0

detector = htm.handDetector()
while True:
    ret, img = cap.read()
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = detector.findHands(img)
    lmList = detector.findPositions(img)

    if len(lmList) > 0:
        # id = 2 is for the index tip and id = 4 is for thumb tip
        x1, y1 = lmList[8][1], lmList[8][2]
        x2, y2 = lmList[4][1], lmList[4][2]

        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

        cx, cy = (x2 + x1) // 2, (y2 + y1) // 2

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        if length < 50:
            cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

        vol = np.interp(length, [50, 300], [minvol, maxvol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])
        # print(length, vol)

        volume.SetMasterVolumeLevel(vol, None)

    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'{str(int(volPer))}%', (40, 450), cv2.FONT_HERSHEY_PLAIN, 2, (255, 250, 250), 2)

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, f'FPS:{str(int(fps))}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 10, 55), 2)
    cv2.imshow('HandVideo', img)

    if cv2.waitKey(10) == ord('q'):
        break
