import cv2
import numpy as np
import face_recognition
import os

path="C:/Users/Jhanvi/Desktop/Facial_Recognization/Project_V-main/demo/static/images"
images=[]
classNames=[]
mylist =os.listdir(path)
print(mylist)

