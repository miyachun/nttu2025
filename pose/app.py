from flask import Flask, Response, render_template
import cv2
import numpy as np
import mediapipe as mp

app = Flask(__name__)

# 讀取帽子和上衣透明PNG
hat_img = cv2.imread("static/hat.png", cv2.IMREAD_UNCHANGED)
shirt_img = cv2.imread("static/shirt.png", cv2.IMREAD_UNCHANGED)

cap = cv2.VideoCapture(0)

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False,
                    model_complexity=1,
                    enable_segmentation=False,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5)

def overlay_transparent(bg, overlay, x, y, scale=1.0):
    overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w = overlay.shape[:2]

    # 如果圖片只有3通道，補上alpha
    if overlay.shape[2] == 3:
        alpha_channel = np.ones((h, w), dtype=np.uint8) * 255
        overlay = np.dstack([overlay, alpha_channel])

    # 邊界修正
    if x < 0:
        overlay = overlay[:, -x:]
        w += x
        x = 0
    if y < 0:
        overlay = overlay[-y:, :]
        h += y
        y = 0
    if x + w > bg.shape[1]:
        w = bg.shape[1] - x
        overlay = overlay[:, :w]
    if y + h > bg.shape[0]:
        h = bg.shape[0] - y
        overlay = overlay[:h, :]

    if w <= 0 or h <= 0:
        return bg

    alpha_overlay = overlay[:, :, 3] / 255.0
    alpha_bg = 1.0 - alpha_overlay

    for c in range(3):
        bg[y:y+h, x:x+w, c] = (alpha_overlay * overlay[:, :, c] +
                               alpha_bg * bg[y:y+h, x:x+w, c])
    return bg

def gen_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            h, w, _ = frame.shape
            landmarks = results.pose_landmarks.landmark

            # 眼睛
            left_eye = np.array([landmarks[2].x * w, landmarks[2].y * h])
            right_eye = np.array([landmarks[5].x * w, landmarks[5].y * h])
            eye_center_x = int((left_eye[0] + right_eye[0]) / 2)
            eye_center_y = int((left_eye[1] + right_eye[1]) / 2)

            # 肩膀
            left_shoulder = np.array([landmarks[11].x * w, landmarks[11].y * h])
            right_shoulder = np.array([landmarks[12].x * w, landmarks[12].y * h])
            shoulder_center_x = int((left_shoulder[0] + right_shoulder[0]) / 2)
            shoulder_center_y = int((left_shoulder[1] + right_shoulder[1]) / 2)

            # 帽子大小

            HAT_SCALE = 3.2    # 帽子放大倍率
            SHIRT_SCALE = 1.5  # 上衣放大倍率
            eye_dist = np.linalg.norm(left_eye - right_eye)
            head_width = int(eye_dist * HAT_SCALE)
            scale_hat = head_width / hat_img.shape[1]



            # 上衣大小
            shoulder_dist = np.linalg.norm(left_shoulder - right_shoulder)
            shirt_width = int(shoulder_dist * SHIRT_SCALE)
            scale_shirt = shirt_width / shirt_img.shape[1]

            # 上衣往上修正 (用肩膀到眼睛距離)
            shirt_height = int(shirt_img.shape[0] * scale_shirt)
            adjust_y = int(shirt_height * 0.1) + int((shoulder_center_y - eye_center_y) * 0.5)

            # 疊加帽子
            frame = overlay_transparent(frame, hat_img,
                                        eye_center_x - head_width//2,
                                        eye_center_y - int(hat_img.shape[0]*scale_hat),
                                        scale_hat)

            # 疊加上衣
            frame = overlay_transparent(frame, shirt_img,
                                        shoulder_center_x - shirt_width//2,
                                        shoulder_center_y - adjust_y,
                                        scale_shirt)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
