
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
import pyttsx3


#--------------------------------------------------------------------

bot = pyttsx3.init()
voice = bot.getProperty('voices')
bot.setProperty('voice',voice[1].id) # chon giong nu
def speak(audio):
    print('BOT : ')
    print(audio)
    bot.say(audio)
    bot.runAndWait()
#speak("hello")
def Welcome():
    hour = datetime.now().hour
    if hour>=0 and hour<12:
        speak("Good Morning everyone")
    elif hour>=12 and hour<18:
        speak("Good Afternoon everyone")
    elif hour >= 18 and hour < 24:
        speak("Good Night everyone")
Welcome()

face_cascade = cv2.CascadeClassifier('library/khuon_mat.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer/huanluyen.yml")

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
window.geometry("800x400")
window.iconbitmap("Image/UET-logo.ico")

bg_loading = Image.open("Image/background.jpg")
bg_render = ImageTk.PhotoImage(bg_loading)
bg = Label(window,image=bg_render)
bg.place(x=00,y=00)

video =cv2.VideoCapture(0)
canvas_w = video.get(cv2.CAP_PROP_FRAME_WIDTH)//2.5
canvas_h = video.get(cv2.CAP_PROP_FRAME_HEIGHT)//2.5
canvas = Canvas(window,width = canvas_w,height = canvas_h, bg ="#EEDD2F")
#canvas.pack(pady = 10)
canvas.place(x=49,y=45)
photo = None

note_lbl = Label(window,text="Please look directly at the camera ",font=("Goudy old style",15,"italic"),fg="#d77337")
note_lbl.place(x=54,y=242)

# lbl_id = Label(window,text="ID",font=("Goudy old style",13,"bold"),bg ="white",fg="gray").place(x=30,y=165)
txt_id = Entry(window,font=("times new roman",13,"bold"),bg="light gray")
txt_id.place(x=139,y=285,width=78,height=30)

frame_info = Frame(window,bg="white")
frame_info.place(x=400,y=40,height=300,width=350)
frame_title = Label(frame_info,text="Information",font=("Impact",35,"bold"),fg="#d77337",bg="white").place(x=30,y=15)
desc = Label(frame_info,text="Time deals gently only with those who take it gently")
desc.config(font=("Goudy old style",10,"bold"),fg="#d77337",bg="white")
desc.place(x=30,y=70)

lbl_username = Label(frame_info,text="Name",font=("Goudy old style",13,"bold"),bg ="white",fg="gray").place(x=30,y=110)
txt_username = Entry(frame_info,font=("times new roman",13,"italic","bold"),bg="light gray")
txt_username.place(x=100,y=110,width=200,height=25)

lbl_age = Label(frame_info,text="D.o.B",font=("Goudy old style",13,"bold"),bg ="white",fg="gray").place(x=30,y=145)
txt_age = Entry(frame_info,font=("times new roman",13,"italic","bold"),bg="light gray")
txt_age.place(x=100,y=145,width=200,height=25)

lbl_gender = Label(frame_info,text="Gender",font=("Goudy old style",13,"bold"),bg ="white",fg="gray").place(x=30,y=180)
txt_gender = Entry(frame_info,font=("times new roman",13,"italic","bold"),bg="light gray")
txt_gender.place(x=100,y=180,width=200,height=25)

lbl_position = Label(frame_info,text="Position",font=("Goudy old style",13,"bold"),bg ="white",fg="gray").place(x=30,y=215)
txt_position = Entry(frame_info,font=("times new roman",13,"italic","bold"),bg="light gray")
txt_position.place(x=100,y=215,width=200,height=25)

lbl_attendanceTime = Label(frame_info,text="A.Time",font=("Goudy old style",13,"bold"),bg ="white",fg="gray").place(x=30,y=250)
txt_attendanceTime = Text(frame_info,font=("times new roman",13,"bold","italic"),bg="light gray")
txt_attendanceTime.place(x=100,y=250,width=200,height=25)


# export_btn = Button(window,text="Export",font=("times new roman",13),fg="white",bg="#d77337").place(x=225,y=538)

# function to change tkinter entry text
def changeEntryText(entry, text):
    try:
        entry.delete(0,END)
    except:
        entry.delete('1.0', END)
        #speak("hello")
    entry.insert(END,text)



def markAttendance(name):
    with open('Record.csv','r+') as f:
        myDataList = f.readline()
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
            print(str(profile[2]))
            print(str(profile[3]))
            print(str(profile[4]))
            # txt_username.insert(END, str(profile[1]))
            changeEntryText(txt_username, str(profile[1]))
            # txt_id.insert(END, str(profile[0]))
            changeEntryText(txt_id, str(profile[0]))
            changeEntryText(txt_age, str(profile[2]))
            changeEntryText(txt_gender, str(profile[3]))
            changeEntryText(txt_position, str(profile[4]))

            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            changeEntryText(txt_attendanceTime, dt_string)
            markAttendance(str(profile[1]))

        else:
            print("unknown")

    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(gray))
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

    window.after(15, updateFrame)

updateFrame()

window.mainloop()
speak("Good bye")



