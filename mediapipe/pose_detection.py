import cv2
import mediapipe as mp

capture = cv2.VideoCapture("videos/dance.mp4")
# capture = cv2.VideoCapture("videos/pexels-tima-miroshnichenko-6572835.mp4")
draw = mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()
frame_width = int(capture.get(3))
frame_height = int(capture.get(4))
size = (frame_width, frame_height)
result = cv2.VideoWriter("output/dance.avi", cv2.VideoWriter_fourcc(*"MJPG"), 10, size)
while True:
    success, img = capture.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    if results.pose_landmarks:
        # print(results.pose_landmarks.landmark)
        draw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
    cv2.imshow("Image", img)
    result.write(img)
    cv2.waitKey(1)
capture.release()
result.release()
cv2.destroyAllWindows()
