import cv2
from ultralytics import YOLO

model = YOLO("last.pt")

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    results = model.predict(frame, conf=0.5)


    annotated = results[0].plot()
    cv2.imshow("YOLO11 Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()