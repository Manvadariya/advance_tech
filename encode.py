# importing necessary modules
import cv2
import face_recognition
import os
import pickle

# importing images
folderPath = 'Images'
pathList = os.listdir(folderPath)
print(pathList)