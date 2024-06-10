import cv2
from cvzone.FaceDetectionModule import FaceDetector
import serial
import numpy as np
import time

# Initialize camera
cap = cv2.VideoCapture(1)
ws, hs = 1280, 720
cap.set(3, ws)
cap.set(4, hs)

# Verify camera access
if not cap.isOpened():
    print("Camera couldn't Access!!!")
    exit()

# Arduino setup
arduino_port = '/dev/cu.usbserial-140'  # Adjust based on your system
board = serial.Serial(arduino_port, 9600)

# Initialize face detector
detector = FaceDetector()
servoPos = [90, 120]  # Initial servo position
last_update_time = time.time()
update_interval = 1  # Update interval in seconds

while True:
    success, img = cap.read()
    if not success:
        break

    img, bboxs = detector.findFaces(img, draw=False)

    if bboxs:
        # Face detected
        bbox = bboxs[0]['bbox']
        x, y, w, h = bbox
        fx, fy = x + w // 2, y + h // 2  # Face center

        pos = [fx, fy]

        servoX = np.interp(fx, [0, ws], [0, 180])
        servoY = np.interp(fy, [0, hs], [120, 180])

        servoX = np.clip(servoX, 0, 180)
        servoY = np.clip(servoY, 120, 180)

        servoPos[1] = 180 - servoX
        servoPos[0] = servoY

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(img, (fx, fy), 5, (0, 0, 255), cv2.FILLED)
        cv2.putText(img, str(pos), (fx + 15, fy - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        water = 1  # Face detected, set water to 1
    else:
        water = 0  # No face detected, set water to 0

    cv2.putText(img, f'Servo X: {int(servoPos[0])} deg', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.putText(img, f'Servo Y: {int(servoPos[1])} deg', (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    # Update servo positions at defined intervals
    if time.time() - last_update_time > update_interval:
        board.write(f"{int(servoPos[0])},{int(servoPos[1])},w{int(water)}\n".encode())
        last_update_time = time.time()  # Update time

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
