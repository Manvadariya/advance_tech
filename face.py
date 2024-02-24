# importing necessary libraries

import cv2

# capture video from camera (from web cam)
cap = cv2.VideoCapture(1) # put 0 for default

# set video size for capture
cap.set(3, 640)
cap.set(4, 480)

# capture video frame by frame, while q is pressed
while True:
    ret, frame = cap.read()

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
