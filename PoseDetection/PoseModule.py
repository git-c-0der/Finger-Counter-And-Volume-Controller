import cv2
import mediapipe as mp
import time

class poseDetector():

    def __init__(self, mode=False, complexity=1, smooth=False, enable_seg=False,
                 smooth_seg=True, detecConf=0.5, trackConf=0.5):

        self.mode = mode
        self.complexity = complexity
        self.smooth = smooth
        self.enable_seg = enable_seg
        self.smooth_seg = smooth_seg
        self.detecConf = detecConf
        self.trackConf = trackConf

        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth, self.enable_seg,
                 self.smooth_seg, self.detecConf, self.trackConf)
        self.mpDraw = mp.solutions.drawing_utils


    def findPose(self, img, draw=True):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = self.pose.process(img)
        if results.pose_landmarks and draw:
            self.mpDraw.draw_landmarks(img, results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img

    def findPosition(self, img, draw=True):
        lmList=[]
        results = self.pose.process(img)
        if results.pose_landmarks:

            for id, lm in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 10, 254), cv2.FILLED)
        return lmList

def main():
    cap = cv2.VideoCapture('PoseVideos/Vid2.mp4')

    ptime = 0
    detector = poseDetector()
    while True:
        ret, img = cap.read()
        img = cv2.resize(img, (640, 480))

        img = detector.findPose(img)
        lmList = detector.findPosition(img, False)
        if len(lmList)>0:
            print(lmList[14])
            cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (255, 10, 254), cv2.FILLED)

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(img, str(int(fps)), (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (255, 154, 200), 3)
        cv2.imshow('Video1', img)

        # cv2.waitKey(1)
        if cv2.waitKey(1) == ord('q'):
            break

if __name__ == '__main__':
    main()
