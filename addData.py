import numpy as np
import os
import sqlite3
import cv2
import numpy as np
import os
import pickle, sqlite3
import cv2
import tkinter
from tkinter import *
#import pillow
import PIL.Image # cài đặt pillow
import PIL.ImageTk
from PIL import Image,ImageTk
#--------------------------------------------------------------------
# CODE NHAP DU LIEU HINH ANH VA DAT TEN KET NOI CO SO DU LIEU
def insertOrUpdate(id, name, dob, gender,position):
    #connecting to the db
    conn =sqlite3.connect("FaceBase.db")
    #check if id already exists
    query = "SELECT * FROM People WHERE ID="+str(id)
    #returning the data in rows
    cursor = conn.execute(query)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if isRecordExist==1:
        query="UPDATE People SET Name="+str(name)+",DateofBirth="+str(dob)+",Gender="+str(gender)+",Position="+str(position)+"WHERE ID="+str(id)
    else:
        query="INSERT INTO People(ID, Name) VALUES('"+str(id)+"','"+str(name)+"','"+str(dob)+"','"+str(gender)+"','"+str(position)+"')"
    print(query)
    conn.execute(query)
    conn.commit()
    conn.close()


face_cascade = cv2.CascadeClassifier('library/khuon_mat.xml')
cap = cv2.VideoCapture(0)
id = input('Mã nhân viên : ')
name = input('Họ tên nhân viên : ')
dob = input('Năm sinh : ')
gender = input('Giới tính : ')
position = input('Chức vụ : ')
print("Bắt đầu lấy dữ liệu khuôn mặt ! ")
print("Vui lòng nhìn thẳng vào máy quay . . .")
insertOrUpdate(id, name, dob, gender, position)
sample_number = 0


while True:
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    img = cv2.resize(img, dsize=None, fx=0.8, fy=0.8)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        sample_number += 1

        if not os.path.exists('data_face'):
            os.makedirs('data_face')

        cv2.imwrite('data_face/User.'+str(id)+"."+str(sample_number)+".jpg",  img[y:y+h,x:x+w])
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)


    cv2.imshow('Adding faces data interface', img)
    cv2.waitKey(1);
    # Check xem có bấm q hoặc trên 100 ảnh sample thì thoát
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    elif sample_number > 100:
        break
cap.release()
cv2.destroyAllWindows()

