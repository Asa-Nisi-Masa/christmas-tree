import sys
import time
from pathlib import Path

import cv2
import requests

from christmas_tree.common.settings import RPI_IP_ADDRESS, TOTAL_LEDS

ANGLE = int(sys.argv[1])

dir_ = Path("frames") / str(ANGLE)

if not dir_.exists():
    dir_.mkdir(parents=True, exist_ok=True)

cap = cv2.VideoCapture(0)

if cap.isOpened():
    running, frame = cap.read()
else:
    running = False


time.sleep(5)
for led_index in range(TOTAL_LEDS):
    path = dir_ / f"{led_index}.jpg"

    response = requests.post(f"{RPI_IP_ADDRESS}/fire/{led_index}")
    if response.status_code != 204:
        print("Something went wrong!")
        break

    time.sleep(0.1)
    running, frame = cap.read()
    cv2.imwrite(str(path), frame)
    cv2.imshow("preview", frame)
    time.sleep(0.1)

    response = requests.delete(f"{RPI_IP_ADDRESS}/fire/{led_index}")
    if response.status_code != 204:
        print("Something went wrong!")
        break

    key = cv2.waitKey(20)
    if key == 27:
        break


cv2.destroyAllWindows()
cap.release()
