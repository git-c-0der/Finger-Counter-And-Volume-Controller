import cv2
import mediapipe as mp
import time


class faceMeshDetector():
    def __init__(self, mode=False, maxFace=1, refLms=False, minDetec=0.5, minTrack=0.5):
        self.mode = mode
        self.maxFace = maxFace
        self.refLms = refLms
        self.minDetec = minDetec
        self.minTrack = minTrack

        self.mpfm = mp.solutions.face_mesh
        self.mpDraw = mp.solutions.drawing_utils
        self.detect = self.mpfm.FaceMesh(self.mode, self.maxFace, self.refLms,
                                         self.minDetec, self.minTrack)
        self.drawSpec = self.mpDraw.DrawingSpec(color=(255, 10, 211), thickness=1, circle_radius=1)

    def findFaceMesh(self, img, draw=True):



        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        faces = []
        results = self.detect.process(img)
        if results.multi_face_landmarks:
            for faceLms in results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms, self.mpfm.FACEMESH_CONTOURS,
                                          self.drawSpec, self.drawSpec)

                face = []
                for id, lm in enumerate(faceLms.landmark):
                    # print(lm)
                    h, w, c = img.shape
                    x, y = int(lm.x * w), int(lm.y * h)
                    cv2.putText(img, str(id), (x, y), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 1)
                    face.append([x, y])
                faces.append(face)

        return img, faces


def main():
    cap = cv2.VideoCapture('PoseVideos/Vid5.mp4')
    ptime = 0

    detector = faceMeshDetector(maxFace=2)
    while True:
        ret, img = cap.read()
        img = cv2.resize(img, (740, 640))
        img, faces = detector.findFaceMesh(img)
        if len(faces) > 0:
            print(len(faces))

        ctime = time.time()
        fps = 0
        if ctime - ptime > 0:
            fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(img, f'FPS:{int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
        cv2.imshow('Video', img)

        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == '__main__':
    main()
