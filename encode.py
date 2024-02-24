# importing necessary modules
import cv2
import face_recognition
import os
import pickle

# Importing student images
# NOTE :- Image size should be 216x216 and name should be id of students
folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)

imgList = []
studentIds = []

for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

# print(studentIds)

# Finding encoding of face
def findEncodings(imgList):
    encodList = []
    for img in imgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(img)

        if len(face_encodings) > 0:
            encod = face_encodings[0]
            encodList.append(encod)
        else:
            print(f"No face found in {img}")
            # You might want to handle this case, depending on your requirements.

    return encodList


print("Start Encodings")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown,studentIds]
print(encodeListKnownWithIds)
print("Done Encoding")

# Storing encoding in separate file
file = open("EncodeFiles.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")