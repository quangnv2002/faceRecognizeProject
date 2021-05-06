import numpy as np
import os
import sqlite3
import cv2
#--------------------------------------------------------------------
# CODE NHAP DU LIEU HINH ANH VA DAT TEN KET NOI CO SO DU LIEU
def insertOrUpdate(id, name):
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
        query="UPDATE People SET Name="+str(name)+" WHERE ID="+str(id)
    else:
        query="INSERT INTO People(ID, Name) VALUES("+str(id)+","+str(name)+")"
    conn.execute(query)
    conn.commit()
    conn.close()


face_cascade = cv2.CascadeClassifier('thuvien/khuon_mat.xml')
cap = cv2.VideoCapture(0)
id = input('Enter user id: ')
name = input('Enter name: ')
insertOrUpdate(id, name)
sample_number = 0
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        sample_number += 1

        if not os.path.exists('data_face'):
            os.makedirs('data_face')

        cv2.imwrite('data_face/User.'+str(id)+"."+str(sample_number)+".jpg",  img[y:y+h,x:x+w])
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(1);
    if(sample_number>100):
        cap.release()
        cv2.destroyAllWindows()
        break;


# import cv2
# import sqlite3
# import tkinter
# from tkinter import *
# from PIL import Image,ImageTk
# import cv2
# import PIL.Image # cài đặt pillow
# import PIL.ImageTk
#
# faceDetect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#
# # cap nhat ten va ID vao csdl
# def InsertOrUpdate(id,name):
#     connect = sqlite3.connect("FaceBaseNew.db")
#     cursor = connect.execute('SELECT * FROM People WHERE ID= '+ str(id))
#     isRecordExist = 0
#     for row in cursor:
#         isRecordExist = 1
#         break;
#     if isRecordExist==1:
#         cmd = "UPDATE people SET Name=' "+str(name)+" ' WHERE ID="+str(id)
#     else:
#         cmd = "INSERT INTO people(ID,Name) Values("+str(id)+",' " + str(name)+" ' )"
#     connect.execute(cmd)
#     connect.commit()
#     connect.close()
#
#
# window = Tk()
# window.title("Giao diện thêm nhân viên")
# window.resizable(False,False)
# window.geometry("500x600")
# window.iconbitmap("Image/UET-logo.ico")
#
# bg_loading = Image.open("Image/background.jpg")
# bg_render = ImageTk.PhotoImage(bg_loading)
# bg = Label(window,image=bg_render)
# bg.place(x=00,y=00)
#
# camera =cv2.VideoCapture(0)
# canvas_w = camera.get(cv2.CAP_PROP_FRAME_WIDTH)//2.5
# canvas_h = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)//2.5
# canvas = Canvas(window,width = canvas_w,height = canvas_h, bg ="#EEDD2F")
# canvas.pack(pady = 10)
#
# photo = None
# sampleNum = 0
# onStart = False
# def updateFrame():
#     global canvas, photo
#
#     # Đọc từ Camera
#     ret, img = camera.read()
#     # Lật ảnh cho đỡ bị ngược
#     img = cv2.flip(img, 1)
#     # Resize
#     img = cv2.resize(img, dsize=None, fx=0.5,fy=0.5)
#     # Đưa ảnh về ảnh xám
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     faces = faceDetect.detectMultiScale(gray, 1.3, 5)
#     if(onStart == True):
#         for (x, y, w, h) in faces:
#             # Vẽ hình chữ nhật quanh mặt nhận được
#             cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
#             sampleNum = sampleNum + 1
#         # Ghi dữ liệu khuôn mặt vào thư mục dataSet
#         cv2.imwrite("dataSet/" + name + '.' + txt_id + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
#
#
#
#     photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(gray))
#     canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
#     window.after(15, updateFrame)
# updateFrame()
#
#
# note_lbl = Label(window,text="Please look directly at the camera ",font=("Goudy old style",15,"italic"),fg="#d77337")
# note_lbl.place(x=125,y=206.5)
#
# frame_info = Frame(window,bg="white")
# frame_info.place(x=80,y=250,height=250,width=350)
# frame_title = Label(frame_info,text="Add New User",font=("Impact",30,"bold"),fg="#d77337",bg="white").place(x=30,y=30)
# desc = Label(frame_info,text="Welcome to our company !!!")
# desc.config(font=("Goudy old style",12,"bold"),fg="#d77337",bg="white")
# desc.place(x=30,y=80)
#
# lbl_username = Label(frame_info,text="Name",font=("Goudy old style",13,"bold"),bg ="white",fg="gray").place(x=30,y=110)
# txt_username = Entry(frame_info,font=("times new roman",15),bg="light gray")
# txt_username.place(x=30,y=135,width=250,height=30)
# name = txt_username.get()
#
# lbl_id = Label(frame_info,text="ID",font=("Goudy old style",13,"bold"),bg ="white",fg="gray").place(x=30,y=165)
# txt_id = Entry(frame_info,font=("times new roman",15),bg="light gray")
# txt_id.place(x=30,y=190,width=250,height=30)
#
# def startBtn():
#     print('Bắt đầu chụp ảnh hồ sơ, nhấn Q để thoát...')
#     onStart = True
#     ID = txt_id.get()
#     name = txt_username.get()
#     print(name)
#     print(ID)
#     InsertOrUpdate(ID,name)
#     onStart = False
#
#
#
# start_btn = Button(window,text="Start",font=("times new roman",13),fg="white",bg="#d77337",command=startBtn).place(x=225,y=538)
#
#
#
# # while(True):
# #
# #     ret, img = camera.read()
# #
# #     # Lật ảnh cho đỡ bị ngược
# #     img = cv2.flip(img,1)
# #
# #     # Kẻ khung giữa màn hình để người dùng đưa mặt vào khu vực này
# #     centerH = img.shape[0] // 2;
# #     centerW = img.shape[1] // 2;
# #     sizeboxW = 300;
# #     sizeboxH = 400;
# #     cv2.rectangle(img, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
# #                   (centerW + sizeboxW // 2, centerH + sizeboxH // 2), (255, 255, 255), 5)
# #
# #     # Đưa ảnh về ảnh xám
# #     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# #
# #     # Nhận diện khuôn mặt
# #     faces = faceDetect.detectMultiScale(gray, 1.3, 5)
# #     for (x, y, w, h) in faces:
# #         # Vẽ hình chữ nhật quanh mặt nhận được
# #         cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
# #         sampleNum = sampleNum + 1
# #         # Ghi dữ liệu khuôn mặt vào thư mục dataSet
# #         cv2.imwrite("dataSet/"+name+'.' + ID + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
# #
# #     cv2.imshow('frame', img)
# #     # Check xem có bấm q hoặc trên 5 ảnh sample thì thoát
# #     if cv2.waitKey(100) & 0xFF == ord('q'):
# #         break
# #     elif sampleNum>5:
# #         break
# #
# # camera.release()
# # cv2.destroyAllWindows()
#
#
# window.mainloop()
