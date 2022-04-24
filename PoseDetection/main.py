import cv2
import mediapipe as mp
import time

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils


cap = cv2.VideoCapture('PoseVideos/Vid1.mp4')

ptime=0
while True:
    ret, img = cap.read()
    img = cv2.resize(img, (640,480))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = pose.process(img)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)

        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (cx, cy), 5, (255,10,254))

    ctime = time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime

    cv2.putText(img, str(int(fps)), (100,100), cv2.FONT_HERSHEY_PLAIN, 3, (255,154,200), 3)
    cv2.imshow('Video1', img)

    # cv2.waitKey(1)
    if cv2.waitKey(1) == ord('q'):
        break
