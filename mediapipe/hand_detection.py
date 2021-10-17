import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
capture = cv2.VideoCapture("videos/sign_language.mp4")
frame_width = int(capture.get(3))
frame_height = int(capture.get(4))
size = (frame_width, frame_height)
result = cv2.VideoWriter(
    "output/sign_language.avi", cv2.VideoWriter_fourcc(*"MJPG"), 10, size
)
while True:
    success, img = capture.read()
    with mp_hands.Hands(
        static_image_mode=True, max_num_hands=2, min_detection_confidence=0.5
    ) as hands:
        results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if not results.multi_hand_landmarks:
            continue
        frame = img.copy()
    for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style(),
        )
    cv2.imshow("Image", frame)
    result.write(frame)
    cv2.waitKey(1)
capture.release()
result.release()
cv2.destroyAllWindows()

# # For webcam input:
# cap = cv2.VideoCapture(0)
# with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
#     while cap.isOpened():
#         success, image = cap.read()
#         if not success:
#             print("Ignoring empty camera frame.")
#             # If loading a video, use 'break' instead of 'continue'.
#             continue

#         # To improve performance, optionally mark the image as not writeable to
#         # pass by reference.
#         image.flags.writeable = False
#         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#         results = hands.process(image)

#         # Draw the hand annotations on the image.
#         image.flags.writeable = True
#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#         if results.multi_hand_landmarks:
#             for hand_landmarks in results.multi_hand_landmarks:
#                 mp_drawing.draw_landmarks(
#                     image,
#                     hand_landmarks,
#                     mp_hands.HAND_CONNECTIONS,
#                     mp_drawing_styles.get_default_hand_landmarks_style(),
#                     mp_drawing_styles.get_default_hand_connections_style(),
#                 )
#         # Flip the image horizontally for a selfie-view display.
#         cv2.imshow("MediaPipe Hands", cv2.flip(image, 1))
#         if cv2.waitKey(5) & 0xFF == 27:
#             break
# cap.release()
