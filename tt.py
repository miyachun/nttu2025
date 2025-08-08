import cv2
from ultralytics import YOLO

# 載入自訂的 last.pt 模型
model = YOLO("last.pt")

# 啟用 webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # 執行偵測
    results = model.predict(frame, conf=0.5)

    # 繪圖與標注
    annotated = results[0].plot()
    cv2.imshow("YOLO11 Detection", annotated)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
