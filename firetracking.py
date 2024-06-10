import cv2
import numpy as np
import torch
import serial
import time
from torchvision import transforms
from ultralytics import YOLO

# Kamera ayarları
cap = cv2.VideoCapture(1)
ws, hs = 1280, 720
cap.set(3, ws)
cap.set(4, hs)

# Arduino ayarları
arduino_port = '/dev/cu.usbserial-110'
board = serial.Serial(arduino_port, 9600)

# Modeli yükle
model = YOLO('best.pt')

servoPos = [90, 120]
last_update_time = time.time()
update_interval = 0.1

while True:
    success, img = cap.read()
    if not success:
        break

    # Görüntüyü modelin giriş boyutlarına yeniden boyutlandır
    results = model(img)
    detections = results[0].boxes.data

    is_fire_detected = False

    for detection in detections:
        class_id = int(detection[-1])
        if class_id == 0:  # Alev sınıfı ID'si, modelinize göre değişebilir
            is_fire_detected = True
            bbox = detection[:4].cpu().numpy().astype(int)
            x, y, x2, y2 = bbox
            w, h = x2 - x, y2 - y
            fx, fy = x + w // 2, y + h // 2

            pos = [fx, fy]

            servoX = np.interp(fx, [0, ws], [0, 180])
            servoY = np.interp(fy, [0, hs], [180, 120])

            servoX = np.clip(servoX, 0, 180)
            servoY = np.clip(servoY, 120, 180)

            servoPos[1] = 180 - servoX
            servoPos[0] = servoY

            cv2.rectangle(img, (x, y), (x2, y2), (0, 255, 0), 2)
            cv2.circle(img, (fx, fy), 5, (0, 0, 255), cv2.FILLED)
            cv2.putText(img, str(pos), (fx + 15, fy - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    water = 1 if is_fire_detected else 0

    cv2.putText(img, f'Servo X: {int(servoPos[0])} deg', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    cv2.putText(img, f'Servo Y: {int(servoPos[1])} deg', (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
    print(water)



    board.write(f"{int(servoPos[0])},{int(servoPos[1])},w{int(water)}\n".encode())



    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
