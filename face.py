# importing necessary libraries
import pickle

import cv2
import os

import cvzone
import face_recognition
import numpy as np


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

# Importing the different mode images into a list
folderModePath = 'modes' # relative path of folder
modePathList = os.listdir(folderModePath)
imgModeList = []

# appending all modes to the mode list

for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

# load the encoding file
print("Loading Encoded Files...")
file = open("EncodeFiles.p", 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File loaded successfully")


modeType = 0

# capture video frame by frame, while q is pressed
while True:
    ret, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # detect the face in current frame and compare with encoding face
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)



    # Resize the captured video to the new dimensions
    img = cv2.resize(img, (new_width, new_height))

    # Copy the resized captured video onto the background at the specified coordinates
    imgBackground[start_y:start_y + new_height, start_x:start_x + new_width] = img

    # add mode to the template
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        # iterate encodeCurFrame and faceCurFrame from zip
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(matches)
            # print(faceDis)

            matchIndex = np.argmin(faceDis)
            # print(matchIndex)
            # if find any face matches with draw border around it  
            if matches[matchIndex]:
                # print("Face Detected")
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = (65 + x1, 210 + y1, x2 - x1, y2 - y1)
                cvzone.cornerRect(imgBackground, bbox, rt=0)

    cv2.imshow('frame', imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
