import cv2
import mediapipe as mp

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
capture = cv2.VideoCapture("videos/man_driving.mp4")
frame_width = int(capture.get(3))
frame_height = int(capture.get(4))
size = (frame_width, frame_height)
result = cv2.VideoWriter(
    "output/man_driving.avi", cv2.VideoWriter_fourcc(*"MJPG"), 10, size
)
while True:
    success, img = capture.read()
    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5
    ) as face_detection:
        results = face_detection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if not results.detections:
        continue
    frame = img.copy()
    for detection in results.detections:
        mp_drawing.draw_detection(frame, detection)
    cv2.imshow("Image", frame)
    result.write(frame)
    cv2.waitKey(1)
capture.release()
result.release()
cv2.destroyAllWindows()
