import math
import time
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

cap = cv2.VideoCapture(1)
detector = HandDetector(maxHands=2, detectionCon=0.8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
# volume.SetMasterVolumeLevel(-96.0, None)
minVol = volRange[0]
maxVol = volRange[1]

pTime = 0

volPer = 0

while True:
    success, img = cap.read()

    # ===== Hand Detector =====
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        # print(lmList[4], lmList[8])
        # print(lmList[8], lmList[12])
        # print(lmList[12], lmList[16])
        # print(lmList[16], lmList[20])

        # Get all fingers positions
        x1, y1 = lmList[4][0], lmList[4][1]
        x2, y2 = lmList[8][0], lmList[8][1]
        x3, y3 = lmList[12][0], lmList[12][1]
        x4, y4 = lmList[16][0], lmList[16][1]
        x5, y5 = lmList[20][0], lmList[20][1]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Link the fingers with a line
        cv2.line(img, (x1, y1), (x2, y2), (173, 173, 173), 3)
        """cv2.line(img, (x2,y2), (x3,y3), (173, 173, 173), 4)
        cv2.line(img, (x3,y3), (x4,y4), (173, 173, 173), 4)
        cv2.line(img, (x4,y4), (x5,y5), (173, 173, 173), 4)"""

        cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        # Hand range from 30 - 300
        # Volume range -96 - 0

        # ===== Volume section =====
        vol = np.interp(length, [100, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])

        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 40:
            cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)

        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)

        cv2.putText(img, f'{int(volPer)} %', (50, 430), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)

        # Make a circle for all fingers
        cv2.circle(img, (x1, y1), 5, (0, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 5, (255, 0, 0), cv2.FILLED)
        cv2.circle(img, (x3, y3), 5, (0, 255, 0), cv2.FILLED)
        cv2.circle(img, (x4, y4), 5, (255, 255, 0), cv2.FILLED)
        cv2.circle(img, (x5, y5), 5, (255, 0, 255), cv2.FILLED)

    # ===== UI =====
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (20, 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1)
    cv2.putText(img, "Press and hold 'x' to quit", (20, 460), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1)
    # ==============

    if lmList:
        fingers = detector.fingersUp()
        # print(fingers)

    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

    cv2.imshow("CvCamera", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
