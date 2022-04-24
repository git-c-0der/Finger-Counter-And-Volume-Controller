import cv2
import mediapipe as mp
import time

class faceDetector():
    def __init__(self, min_detection_confidence=0.5, model_selection=0):
        self.min_detection_confidence = min_detection_confidence
        self.model_selection = model_selection

        self.mpfd = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.detect = self.mpfd.FaceDetection(self.min_detection_confidence)

    def findFaces(self, img, draw=True):

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.detect.process(img)
        bboxs = []

        if results.detections:
            for id, detections in enumerate(results.detections):
                h, w, c = img.shape
                bboxC = detections.location_data.relative_bounding_box
                bbox = int(bboxC.xmin*w), int(bboxC.ymin*h), \
                        int(bboxC.width*w), int(bboxC.height*h)
                bboxs.append([id, bbox, detections.score])

                if draw:
                    img = self.fancyDraw(img, bbox)
                    cv2.putText(img, f'{int(detections.score[0] * 100)}%', (bbox[0], bbox[1]-20),
                                cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 2)

        return img, bboxs

    def fancyDraw(self, img, bbox, l=30, t=5):
        x, y, w, h = bbox
        x1, y1 = x+w, y+h

        cv2.rectangle(img, bbox, (255, 0, 255), 1)

        # Top Left
        cv2.line(img, (x, y), (x+l, y), (255,100,255), t)
        cv2.line(img, (x, y), (x, y+l), (255,100,255), t)

        # Bottom Right
        cv2.line(img, (x1, y1), (x1 - l, y1), (255, 100, 255), t)
        cv2.line(img, (x1, y1), (x1, y1 - l), (255, 100, 255), t)

        return img

def main():
    cap = cv2.VideoCapture('PoseVideos/Vid5.mp4')
    ptime = 0

    detector = faceDetector(0.75, 1)
    while True:
        ret, img = cap.read()
        img = cv2.resize(img, (800, 600))
        img, bboxs = detector.findFaces(img)

        ctime = time.time()
        fps = 0
        if ctime - ptime > 0:
            fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(img, f'FPS:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
        cv2.imshow('Video', img)

        if cv2.waitKey(10) == ord('q'):
            break



if __name__=='__main__':
    main()