import cv2
import mediapipe as mp
import numpy as np
import tempfile
import math

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)       # Flask app initialized
CORS(app)                   # Allow frontend (React) to access this API

# ✅ Test Route to confirm backend is running
@app.route('/')
def home():
    return "Backend is running!"

# ✅ Main route to analyze posture from uploaded video
@app.route('/analyze', methods=['POST'])
def analyze_posture():
    if 'video' not in request.files:
        return jsonify({"error": "No video uploaded"}), 400

    video_file = request.files['video']

    # ✅ Check if posture_type is given (default to 'squat')
    posture_type = request.form.get("posture_type", "squat")

    # ✅ Save uploaded video to temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    video_file.save(temp_file.name)

    cap = cv2.VideoCapture(temp_file.name)

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()

    bad_postures = 0
    total_frames = 0

    # ✅ Helper function to calculate angle between 3 keypoints
    def get_angle(a, b, c):
        a = np.array([a.x, a.y])
        b = np.array([b.x, b.y])
        c = np.array([c.x, c.y])

        ba = a - b
        bc = c - b

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)
        return np.degrees(angle)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        total_frames += 1
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = pose.process(image_rgb)

        if result.pose_landmarks:
            landmarks = result.pose_landmarks.landmark

            shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
            knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
            ear = landmarks[mp_pose.PoseLandmark.LEFT_EAR]

            # ✅ Rule for Squat posture
            if posture_type == "squat":
                back_angle = get_angle(shoulder, hip, knee)
                if back_angle < 150:
                    bad_postures += 1

            # ✅ Rule for Desk Sitting posture
            elif posture_type == "desk":
                neck_angle = get_angle(ear, shoulder, hip)
                back_angle = get_angle(shoulder, hip, knee)

                if neck_angle > 30 or back_angle < 150:
                    bad_postures += 1

    cap.release()

    summary = {
        "total_frames": total_frames,
        "bad_posture_frames": bad_postures,
        "bad_posture_percent": round((bad_postures / total_frames) * 100, 2) if total_frames > 0 else 0,
        "posture_type": posture_type
    }

    return jsonify(summary)

# ✅ This actually runs the Flask development server
if __name__ == '__main__':
    app.run(debug=True)