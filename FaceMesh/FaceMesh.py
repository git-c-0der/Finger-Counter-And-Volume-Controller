import cv2
import mediapipe as mp
import time

mpfm = mp.solutions.face_mesh
mpDraw = mp.solutions.drawing_utils
detect = mpfm.FaceMesh(max_num_faces=2)
drawSpec = mpDraw.DrawingSpec(color=(255,10,211), thickness=1, circle_radius=1)

cap = cv2.VideoCapture('PoseVideos/Vid5.mp4')
ptime = 0
while True:
    ret, img = cap.read()
    img = cv2.resize(img, (740, 640))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = detect.process(img)
    if results.multi_face_landmarks:
        for faceLms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img, faceLms, mpfm.FACEMESH_CONTOURS,
                                  drawSpec, drawSpec)

            for id, lm in enumerate(faceLms.landmark):
                # print(lm)
                h, w, c = img.shape
                x, y = int(lm.x * w), int(lm.y * h)
                print(id, x, y)

    ctime = time.time()
    fps = 0
    if ctime - ptime > 0:
        fps = 1/(ctime - ptime)
    ptime = ctime

    cv2.putText(img, f'FPS:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
    cv2.imshow('Video', img)

    if cv2.waitKey(1) == ord('q'):
        break