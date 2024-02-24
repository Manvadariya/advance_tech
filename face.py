# importing necessary libraries
import cv2

# capture video from camera (from web cam)
cap = cv2.VideoCapture(1)  # put 0 for default

# set video size for capture
cap.set(3, 750)
cap.set(4, 1000)

# importing background image
imgBackground = cv2.imread(r"background.jpg")

# Set the exact pixel coordinates for the starting position
start_x = 0  # Specify the exact X-coordinate
start_y = 192   # Specify the exact Y-coordinate

# Set the new dimensions for the captured video
new_width = 753
new_height = 528

# capture video frame by frame, while q is pressed
while True:
    ret, img = cap.read()

    # Resize the captured video to the new dimensions
    img = cv2.resize(img, (new_width, new_height))

    # Copy the resized captured video onto the background at the specified coordinates
    imgBackground[start_y:start_y + new_height, start_x:start_x + new_width] = img

    cv2.imshow('frame', imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
