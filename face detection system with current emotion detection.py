import cv2
import numpy as np
from deepface import DeepFace
import datetime
import os

# Create folder to save faces
if not os.path.exists("saved_faces"):
    os.makedirs("saved_faces")

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start webcam
cap = cv2.VideoCapture(0)

face_id = 0

print("Press 's' to save face, 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]

        # Emotion detection using DeepFace
        try:
            result = DeepFace.analyze(face, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']
        except:
            emotion = "N/A"

        # Draw rectangle and put emotion text
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"Emotion: {emotion}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # Blur face for privacy (optional)
        # face_blur = cv2.GaussianBlur(face, (99, 99), 30)
        # frame[y:y+h, x:x+w] = face_blur

        # Save face if 's' is pressed
        key = cv2.waitKey(1)
        if key == ord('s'):
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            face_filename = f"saved_faces/face_{timestamp}.jpg"
            cv2.imwrite(face_filename, face)
            print(f"Saved {face_filename}")

    cv2.imshow("Face Detection with Features", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
