# importing necessary libraries
import os
import pickle
import cv2
import cvzone
import face_recognition
import numpy as np
from datetime import datetime
# database
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://faceattendance-c7b33-default-rtdb.firebaseio.com/',
    'storageBucket': 'faceattendance-c7b33.appspot.com'
})

bucket = storage.bucket()
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

mark_attendance_delay = 30*60 # (in seconds)

modeType = 0
counter = 0
id = -1
imgStudent = []
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
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            # print(matches)
            # print(faceDis)

            matchIndex = np.argmin(faceDis)
            # print(matchIndex)

            if matches[matchIndex]:
                # print("Face Detected")
                # print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = (65 + x1, 190 + y1, x2 - x1, y2 - y1)
                cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                if counter == 0:
                    counter = 1
                    modeType = 1
        if counter != 0:

            if counter == 1:
                # get the student Data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                # Get the Image from the storage
                blob = bucket.get_blob(f'Images/{id}.jpeg')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                # Update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                # print(secondsElapsed)

                if secondsElapsed > mark_attendance_delay:
                    ref = db.reference(f'Students/{id}')
                    studentInfo['total_attendance'] += 1
                    ref.child('total_attendance').set(studentInfo['total_attendance'])
                    ref.child('last_attendance_time').set(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if modeType != 3:

                if 10 < counter < 20:
                    modeType = 2

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if counter <= 10:
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861,125), cv2.FONT_HERSHEY_COMPLEX, 1 ,(255,255,255), 1)
                    cv2.putText(imgBackground, str(studentInfo['branch']), (1026,552), cv2.FONT_HERSHEY_COMPLEX, 0.8 ,(255,255,255), 1)
                    cv2.putText(imgBackground, str(id), (1025,496), cv2.FONT_HERSHEY_COMPLEX, 0.8 ,(255,255,255), 1)
                    cv2.putText(imgBackground, str(studentInfo['class']), (910,625), cv2.FONT_HERSHEY_COMPLEX, 0.6 ,(100,100,100), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1025,625), cv2.FONT_HERSHEY_COMPLEX, 0.6 ,(100,100,100), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125,625), cv2.FONT_HERSHEY_COMPLEX, 0.6 ,(100,100,100), 1)
                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50),
                                1)

                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0


    cv2.imshow('frame', imgBackground)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
