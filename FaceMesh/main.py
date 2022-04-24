import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture('PoseVideos/Vid4.mp4')
mpfd = mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
detect = mpfd.FaceDetection()

ptime = 0
while True:
    ret, img = cap.read()
    img = cv2.resize(img, (800, 600))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = detect.process(img)
    # print(results)

    if results.detections:
        for id, detections in enumerate(results.detections):
            # print(id, detections)
            # mpDraw.draw_detection(img, detections)
            h, w, c = img.shape
            bboxC = detections.location_data.relative_bounding_box
            bbox = int(bboxC.xmin*w), int(bboxC.ymin*h), \
                    int(bboxC.width*w), int(bboxC.height*h)
            cv2.rectangle(img, bbox, (255, 0, 255), 2)
            cv2.putText(img, f'{int(detections.score[0] * 100)}%', (bbox[0], bbox[1]-20),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

    ctime = time.time()
    fps=0
    if ctime-ptime > 0:
        fps = 1/(ctime-ptime)
    ptime = ctime

    cv2.putText(img, f'FPS:{int(fps)}',(20,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 2)
    cv2.imshow('Video', img)

    if cv2.waitKey(10) == ord('q'):
        break
