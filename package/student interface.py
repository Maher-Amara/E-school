import os
import tkinter as tk
from tkinter import ttk
import turtle
from turtle import RawTurtle
import fitz
from PIL import Image, ImageTk
from io import BytesIO
import socket
import threading


# import multiprocessing
# import concurrent.futures

def pdf2img(page_nbr, pdf_path, pdf_name):
    save_path = 'temp/' + pdf_name
    #
    page_nbr_rel = page_nbr % len(doc)
    zoom_x = 2  # horizontal zoom
    zoom_y = 2  # vertical zoom
    path = save_path[:-4] + " p." + str(page_nbr_rel) + ".png"
    stream = BytesIO(doc.loadPage(page_nbr_rel).getPixmap(matrix=fitz.Matrix(zoom_x, zoom_y)).getPNGData())
    return stream, path


def adapt(stream, path):
    # full screan
    CanvHeight1 = 610
    CanvWidth1 = 1232

    image = Image.open(stream)

    Width, Height = image.size
    new_image = image.copy()
    if Width > CanvWidth1:
        new_image = image.copy()
        new_image.thumbnail((CanvWidth1, Height))  # duble check

    Width1, Height1 = new_image.size
    img_list = list()
    if Height1 > CanvHeight1:
        pas = 100
        s = 0
        i = 0
        while s + CanvHeight1 < Height1:
            box = (0, s, Width1, s + CanvHeight1)
            image_temp = new_image.crop(box)
            final_path = path[:-4] + "." + str(i) + ".png"
            img_list += [{'path': final_path, 'image': image_temp}]
            s += pas
            i += 1

        box = (0, Height1 - CanvHeight1, Width1, Height1)
        image_temp = new_image.crop(box)
        final_path = path[:-4] + "." + str(i) + ".png"
        img_list += [{'path': final_path, 'image': image_temp}]
    else:
        final_path = path[:-4] + ".0.png"
        img_list += [{'path': final_path, 'image': new_image}]

    return img_list


def pdf_images(page_n, page_m, pdf_path="assets/PdfFiles/", pdf_name="Cours arduino + TP.pdf"):
    page_stream, page_path = pdf2img(page_n, pdf_path, pdf_name)
    img_list = adapt(page_stream, page_path)
    picpath, image = img_list[page_m % len(img_list)].values()
    return picpath, image


def my_bgpic(picname, image_l):
    screen = t.screen
    screen._bgpics[picname] = ImageTk.PhotoImage(image=image_l)
    screen._setbgpic(screen._bgpic, screen._bgpics[picname])
    screen._bgpicname = picname


def show_frame(page_name):
    page_name.tkraise()
    page_name.focus_set()


def key(event1, event2):
    t.pendown()


def pen_color(color):
    t.pencolor(color)


def bg_image(item):
    if item == 'Board':
        t.screen.bgpic(board)
    elif item == 'PDF':
        path, image = pdf_images(n, m, pdf_path=pdf_path, pdf_name=pdf_name)
        my_bgpic(path, image)


def back():
    nbr_actions = 50
    for _ in range(nbr_actions):
        t.undo()


def clear_board():
    t.clear()


def page_control(page, division):
    """'Up''Down''Next''Previous'"""
    path, image = pdf_images(page, division, pdf_path=pdf_path, pdf_name=pdf_name)
    my_bgpic(path, image)


def execute_data(msg):
    global x, y, n, m
    commande = msg.split()
    print(commande)
    if commande[0] == 'position':
        x, y = float(commande[1]), float(commande[2])
    elif commande[0] == "pendown":
        t.pendown()
    elif commande[0] == "penup":
        t.penup()
    elif commande[0] == "color":
        t.pencolor(commande[1])
    elif commande[0] == "bgimage":
        bg_image(commande[1])
    elif commande[0] == 'back':
        back()
    elif commande[0] == "clear":
        t.clear()
    elif commande[0] == "page":
        n, m = int(commande[1]), int(commande[2])
        page_control(n, m)
    else:
        pass


def receive_data():
    global data_list
    # msglen = int()
    # full_msg = ''
    # new_msg = True
    while True:
        msg = s.recv(50)
        # if new_msg:
        #     msglen = int((msg[:Header_Size]).decode("utf-8"))
        #     new_msg = False
        #
        # full_msg += msg.decode("utf-8")
        # if len(full_msg) - Header_Size == msglen:
        #     new_msg = True
        #     data_list += [full_msg[Header_Size:]]
        #     full_msg = ''
        data_list += [msg.decode("utf-8")]


# create window
window = tk.Tk()
window.title("E-school Student ")
# window.iconbitmap("icone.ico")

# I - side bar
side_bar = tk.Frame(window)
side_bar.pack(fill='y', side='left', anchor='nw', ipadx=10)

button1 = ttk.Button(side_bar, command=lambda: show_frame(WELCOME))
image1 = tk.PhotoImage(file="assets/buttons/student.png")
button1.config(image=image1)
button1.pack(pady=10)

button2 = ttk.Button(side_bar, command=lambda: show_frame(LIVE_CORSE))
image2 = tk.PhotoImage(file="assets/buttons/broadcast.png")
button2.config(image=image2)
button2.pack(pady=10)

button3 = ttk.Button(side_bar, command=lambda: show_frame(PENDING_CORSES))
image3 = tk.PhotoImage(file="assets/buttons/online-course.png")
button3.config(image=image3)
button3.pack(pady=10)

button4 = ttk.Button(side_bar, command=lambda: show_frame(SUPPORT_COUR))
image4 = tk.PhotoImage(file="assets/buttons/folder.png")
button4.config(image=image4)
button4.pack(pady=10)

# copyrights = tk.Label(side_bar, text="made by \n maher \n powered \n by python", font=("courrier", 15), fg='#0C6CAE')
# copyrights.pack(fill='x', side='bottom')

# II - main area
mainarea = tk.Frame(window, bg="#000000")
mainarea.pack(fill='both', expand=True)

# pages of the main area :

# 2- LIVE_CORSE
LIVE_CORSE = tk.Frame(mainarea)
LIVE_CORSE.grid(row=0, column=0, sticky="nsew")

TopBar = tk.Frame(LIVE_CORSE)

start_corse = tk.Button(TopBar, text="start corse")
start_corse.grid(row=0, column=0, padx=10, pady=5)
download = tk.Button(TopBar, text="download PDF")
download.grid(row=0, column=1, padx=10, pady=5)

TopBar.grid(row=0, column=0)

CanvHeight = 610  # full screan
CanvWidth = 1232  # full screan
canvas = tk.Canvas(master=LIVE_CORSE, width=CanvWidth, height=CanvHeight)
canvas.grid(row=1, column=0, sticky="nsew")

BottomBar = tk.Frame(LIVE_CORSE)
sound = tk.Button(BottomBar, text="sound on/off")
sound.grid(row=0, column=0)

send = tk.Button(BottomBar, text='send')
send.grid(row=0, column=1)
BottomBar.grid(row=2, column=0)

# Turtle __INIT__
t: RawTurtle = turtle.RawTurtle(canvas)
t.screen.setworldcoordinates(0, 1, 1, 0)
canvas.itemconfig(t.screen._bgpic, anchor="nw")
t.speed(0)
t.left(-135)
t.penup()
t.pensize(3)

# 3- Pending_CORSES
PENDING_CORSES = tk.Label(mainarea, text="PENDING_CORSES", font=("courrier", 15), bg='#0C6CAE', fg='white')
PENDING_CORSES.grid(row=0, column=0, sticky="nsew")

# 4- SUPPORT DU COUR
borderImageData = '''
    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
'''
style = ttk.Style()
borderImage = tk.PhotoImage("borderImage", data=borderImageData)
style.element_create("RoundedFrame", "image", borderImage, border=16, sticky="nsew")
style.layout("RoundedFrame", [("RoundedFrame", {"sticky": "nsew"})])


def download(wedget):
    FileButton.configure()
    print(wedget)


SUPPORT_COUR = tk.Frame(mainarea, bg='#FFFFFF')
files = os.listdir('assets/PdfFiles')
for i in range(len(files)):
    DownloadFrame = ttk.Frame(SUPPORT_COUR, style="RoundedFrame", padding=10)
    FileLabel = tk.Label(DownloadFrame, text=files[i], font=("courrier", 15), bg='#FFFFFF', fg='#000000')
    FileLabel.grid(row=0, column=0, pady=10, padx=10, sticky='w')
    progress_bar = ttk.Progressbar(DownloadFrame, orient='horizontal', length=200, mode='determinate')
    progress_bar.grid(row=0, column=1, pady=10, padx=10)
    FileButton = ttk.Button(DownloadFrame, style="Toolbutton", text='download', command=lambda: download(files[i]))
    FileButton.grid(row=0, column=2, pady=10, padx=10)
    DownloadFrame.pack(fill='x', anchor='nw', pady=10, padx=20)

SUPPORT_COUR.grid(row=0, column=0, sticky="nsew")

# WELCOME
WELCOME = tk.Label(mainarea, text="welcome", font=("courrier", 15), bg='#0C6CAE', fg='white')
WELCOME.grid(row=0, column=0, sticky="nsew")

# __INIT__
pdf_path = "assets/PdfFiles/"
pdf_name = "Cours arduino + TP.pdf"
doc = fitz.open(pdf_path + pdf_name)
board = "assets/whiteboard.png"
n = 0
m = 0
# server
IP = socket.gethostname()
port = 4250
Header_Size = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, port))

path, image = pdf_images(n, m, pdf_path=pdf_path, pdf_name=pdf_name)
my_bgpic(path, image)

data_list = list()  # you might wonna buffer this (list)

t1 = threading.Thread(target=receive_data)
t1.start()

x, y = -1, -1


def pointer_update():
    global data_list
    while True:
        if data_list:
            data = data_list.pop(0)
            execute_data(data)
            if x != -1:
                t.goto(x, y)
        window.update()


pointer_update()
# window.mainloop()
