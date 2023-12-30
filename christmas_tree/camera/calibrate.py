import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

while cap.isOpened():
    ret, frame = cap.read()

    height, width, _ = frame.shape

    cv2.line(frame, (0, height // 2), (width, height // 2), (0, 255, 0), thickness=1)
    cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 255, 0), thickness=1)

    cv2.imshow("calibration", frame)

    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
