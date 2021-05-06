
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
import csv
from datetime import datetime
#--------------------------------------------------------------------
# CODE KET NOI DU LIEU NHAN DIEN HINH ANH KHUON MAT

face_cascade = cv2.CascadeClassifier('thuvien/khuon_mat.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("huanluyen/huanluyen.yml")

def getProfile(Id):
    conn=sqlite3.connect("FaceBase.db")
    query="SELECT * FROM People WHERE ID="+str(Id)
    cursor=conn.execute(query)
    profile=None
    for row in cursor:
        profile=row
    conn.close()
    return profile


window = Tk()
window.title("Phần mềm điểm danh")
window.resizable(False,False)
window.geometry("500x600")
window.iconbitmap("Image/UET-logo.ico")

bg_loading = Image.open("Image/background.jpg")
bg_render = ImageTk.PhotoImage(bg_loading)
bg = Label(window,image=bg_render)
bg.place(x=00,y=00)

video =cv2.VideoCapture(0)
canvas_w = video.get(cv2.CAP_PROP_FRAME_WIDTH)//2.5
canvas_h = video.get(cv2.CAP_PROP_FRAME_HEIGHT)//2.5
canvas = Canvas(window,width = canvas_w,height = canvas_h, bg ="#EEDD2F")
canvas.pack(pady = 10)

photo = None

note_lbl = Label(window,text="Please look directly at the camera ",font=("Goudy old style",15,"italic"),fg="#d77337")
note_lbl.place(x=125,y=206.5)

frame_info = Frame(window,bg="white")
frame_info.place(x=80,y=250,height=300,width=350)
frame_title = Label(frame_info,text="Information",font=("Impact",30,"bold"),fg="#d77337",bg="white").place(x=30,y=30)
desc = Label(frame_info,text="Time deals gently only with those who take it gently")
desc.config(font=("Goudy old style",10,"bold"),fg="#d77337",bg="white")
desc.place(x=30,y=80)

lbl_username = Label(frame_info,text="Name",font=("Goudy old style",13,"bold"),bg ="white",fg="gray").place(x=30,y=110)
txt_username = Entry(frame_info,font=("times new roman",15),bg="light gray")
txt_username.place(x=30,y=135,width=250,height=30)

lbl_id = Label(frame_info,text="ID",font=("Goudy old style",13,"bold"),bg ="white",fg="gray").place(x=30,y=165)
txt_id = Entry(frame_info,font=("times new roman",15),bg="light gray")
txt_id.place(x=30,y=190,width=250,height=30)

lbl_attendanceTime = Label(frame_info,text="Attendance Time",font=("Goudy old style",13,"bold"),bg ="white",fg="gray").place(x=30,y=220)
txt_attendanceTime = Text(frame_info,font=("times new roman",15),bg="light gray")
txt_attendanceTime.place(x=30,y=245,width=250,height=30)

# export_btn = Button(window,text="Export",font=("times new roman",13),fg="white",bg="#d77337").place(x=225,y=538)

def markAttendance(name):
    with open('Record.csv', 'r+') as f:
        myDataList = []
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString  = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

def updateFrame():
    global canvas,photo
    ret, img = video.read()
    img = cv2.flip(img, 1)
    img = cv2.resize(img, dsize=None, fx=0.5, fy=0.5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # phat hien khuon mat trong anh camera
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # lap qua tat ca khuon mat
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        id, dist = recognizer.predict(gray[y:y + h, x:x + w])


        profile = None
        if (dist < 70):
            profile = getProfile(id)
        if (profile != None):
            print(str(profile[1]))
            print(str(profile[0]))
            txt_username.insert(END, str(profile[1]))
            txt_id.insert(END, str(profile[0]))
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            txt_attendanceTime.insert(END,dt_string)
            # txt_username.delete('1.0', END
            #             mar)kAttendance(str(profile[1]))

            # c = csv.writer(open("Record.csv", "wb"))
            # c.writerow(str(profile[1]))

        else:
            print("unknown")
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(gray))
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

    window.after(15, updateFrame)

updateFrame()
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("Ngay va gio hien tai =", dt_string)
window.mainloop()




