# importing necessary modules
import cv2
import mediapipe as mp

cap = cv2.VideoCapture(1) # Set your camera appropriately by changing count Ex: 0

while True :
    ref, img = cap.read()
    cv2.imshow("Detecting", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()