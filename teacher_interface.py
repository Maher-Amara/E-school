import os
import tkinter as tk
from tkinter import ttk
import turtle
from turtle import RawTurtle
import fitz
from PIL import Image, ImageTk
from io import BytesIO
import socket
import select
import threading


def send_something(msg):
    if connected:
        msg = f'{msg:<50}'
        clientsocket.send(bytes(msg, "utf-8"))


def network_pointer(x, y):  # len = 9
    send_something('position ' + str(x) + ' ' + str(y))


def network_solving(command):
    send_something(command)


def pdf2img(page_nbr, pdf_path, pdf_name):

    save_path = 'temp/' + pdf_name
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


def my_bgpic(picname, image):
    screen = t.screen
    screen._bgpics[picname] = ImageTk.PhotoImage(image=image)
    screen._setbgpic(screen._bgpic, screen._bgpics[picname])
    screen._bgpicname = picname


def show_frame(page_name):
    page_name.tkraise()
    page_name.focus_set()


def pointer_position_wedget(wedget):
    """position of a pointer % widget"""
    coord_W = wedget.winfo_pointerx() - wedget.winfo_rootx() - 2
    coord_H = wedget.winfo_pointery() - wedget.winfo_rooty() - 2
    Wproportion = coord_W / wedget.winfo_width()
    Hproportion = coord_H / wedget.winfo_height()

    if 1 >= Wproportion >= 0 and 1 >= Hproportion >= 0:
        return Wproportion, Hproportion
    else:
        return -1, -1


def key(event1, event2):
    network_solving("pendown ")
    t.pendown()


def key2(event1, event2):
    network_solving("penup ")
    t.penup()


def pen():
    if t.isvisible():
        t.hideturtle()
    else:
        t.showturtle()


def pen_color(item):
    color = PenColor.get()
    network_solving("color " + color)
    t.pencolor(color)


def bg_image(item):
    network_solving("bgimage " + item)
    if item == 'Board':
        t.screen.bgpic(board)
    elif item == 'PDF':
        path, image = pdf_images(n, m, pdf_path=pdf_path, pdf_name=pdf_name)
        my_bgpic(path, image)


def back():
    # more work on this
    # how to count actions
    network_solving('back')
    nbr_actions = 50
    for _ in range(nbr_actions):
        t.undo()


def clear_board():
    network_solving("clear")
    t.clear()


def page_control(item):
    """'Up''Down''Next''Previous'"""
    global n, m

    if item == 'Next':
        n += 1
        m = 0
    elif item == 'Previous':
        n -= 1
        m = 0
    elif item == 'Down':
        m += 1
    elif item == 'Up':
        m -= 1
    network_solving("page " + str(n) + " " + str(m))
    path, image = pdf_images(n, m, pdf_path=pdf_path, pdf_name=pdf_name)
    my_bgpic(path, image)


def connection():
    global clientsocket, adress, connected
    clientsocket, adress = s.accept()
    connected = True
    print(f"connection from {adress} has been established!")
    msg = "welcome to the server mother fucker !"
    msg = f'{len(msg):<{Header_Size}}' + msg
    clientsocket.send(bytes(msg, "utf-8"))


# create window
window = tk.Tk()
window.title("E-school Teacher")
# window.geometry('1366x768+0+0')
# window.iconbitmap("icone.ico")

# I - side bar
side_bar = tk.Frame(window, bg="#FFFFFF")
side_bar.pack(fill='y', side='left', anchor='nw', ipadx=10)

button1 = tk.Button(side_bar, command=lambda: show_frame(WELCOME))
image1 = tk.PhotoImage(file="assets/buttons/student.png")
button1.config(image=image1)
button1.pack(pady=10)

button2 = tk.Button(side_bar, command=lambda: show_frame(LIVE_CORSE))
image2 = tk.PhotoImage(file="assets/buttons/broadcast.png")
button2.config(image=image2)
button2.pack(pady=10)

button4 = tk.Button(side_bar, command=lambda: show_frame(SUPPORT_COUR))
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

Pen = tk.Button(TopBar, text="Pen", command=lambda: pen())
PenImage = tk.PhotoImage(file="assets/buttons/pen.png")
Pen.config(image=PenImage)
Pen.grid(row=0, column=0, padx=10, pady=5)

PenColor = ttk.Combobox(TopBar, width=15, state="readonly")
PenColor['values'] = ('black', 'red', 'green', 'blue')
PenColor.grid(row=0, column=1, padx=5, pady=5)
PenColor.current(0)
PenColor.bind("<<ComboboxSelected>>", pen_color)

Board = tk.Button(TopBar, command=lambda: bg_image('Board'))
image5 = tk.PhotoImage(file="assets/buttons/whiteboard.png")
Board.config(image=image5)
Board.grid(row=0, column=2, padx=5, pady=5)

PDF = tk.Button(TopBar, command=lambda: bg_image('PDF'))
image6 = tk.PhotoImage(file="assets/buttons/pdf.png")
PDF.config(image=image6)
PDF.grid(row=0, column=3, padx=10, pady=5)

Back = tk.Button(TopBar, command=lambda: back())
image7 = tk.PhotoImage(file="assets/buttons/return.png")
Back.config(image=image7)
Back.grid(row=0, column=4, padx=10, pady=5)

ClearBoard = tk.Button(TopBar, command=lambda: clear_board())
image8 = tk.PhotoImage(file="assets/buttons/clean.png")
ClearBoard.config(image=image8)
ClearBoard.grid(row=0, column=5, padx=10, pady=5)

start_end_corse = tk.Button(TopBar, text="start/end corse")
start_end_corse.grid(row=0, column=6, padx=10, pady=5)

TopBar.grid(row=0, column=0)

CanvHeight = 610  # full screan
CanvWidth = 1232  # full screan
canvas = tk.Canvas(master=LIVE_CORSE, width=CanvWidth, height=CanvHeight)
canvas.grid(row=1, column=0, sticky="nsew")

SideBar = tk.Frame(LIVE_CORSE)

Up = tk.Button(SideBar, command=lambda: page_control('Up'))
UpImage = tk.PhotoImage(file='assets/buttons/up.png')
Up.config(image=UpImage)
Up.grid(row=0, column=0)

Down = tk.Button(SideBar, command=lambda: page_control('Down'))
DownImage = tk.PhotoImage(file='assets/buttons/down.png')
Down.config(image=DownImage)
Down.grid(row=1, column=0)
SideBar.grid(row=1, column=1)

BottomBar = tk.Frame(LIVE_CORSE)
Previous = tk.Button(BottomBar, command=lambda: page_control('Previous'))
PreviousImage = tk.PhotoImage(file='assets/buttons/previous.png')
Previous.config(image=PreviousImage)
Previous.grid(row=0, column=0)

Next = tk.Button(BottomBar, command=lambda: page_control('Next'))
NextImage = tk.PhotoImage(file='assets/buttons/next.png')
Next.config(image=NextImage)
Next.grid(row=0, column=1)

mic = tk.Button(BottomBar, text='mic on/off')
mic.grid(row=0, column=2)
BottomBar.grid(row=2, column=0)

# Turtle __INIT__
t: RawTurtle = turtle.RawTurtle(canvas)
t.screen.setworldcoordinates(0, 1, 1, 0)
canvas.itemconfig(t.screen._bgpic, anchor="nw")
t.speed(0)
t.left(-135)
t.hideturtle()
t.penup()
t.pensize(3)

# 4- SUPPORT DU COUR
SUPPORT_COUR = tk.Label(mainarea, text="SUPPORT_COUR", font=("courrier", 15), bg='#0C6CAE', fg='white')
SUPPORT_COUR.grid(row=0, column=0, sticky="nsew")

# WELCOME
WELCOME = tk.Label(mainarea, text="welcome", font=("courrier", 15), bg='#0C6CAE', fg='white')
WELCOME.grid(row=0, column=0, sticky="nsew")

# __INIT__
pdf_path = "assets/PdfFiles/cours/matiere (1)/"
pdf_name = "Cours arduino + TP.pdf"
doc = fitz.open(pdf_path + pdf_name)
board = "assets/whiteboard.png"
n = 0
m = 0

path, image = pdf_images(n, m, pdf_path=pdf_path, pdf_name=pdf_name)
my_bgpic(path, image)

# server
IP = socket.gethostname()  # "127.0.0.1"
port = 4250
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, port))
s.listen(5)
Header_Size = 10

clientsocket = socket.socket()
adress = str()
connected = False

t1 = threading.Thread(target=connection, daemon=True)
t1.start()


def pointer_update():
    while True:
        try:
            x, y = pointer_position_wedget(canvas)
        except tk.TclError:
            break
        # network_pointer(x, y)
        if x == -1:
            if t.isdown():
                t.penup()
        else:
            network_pointer(x, y)
            t.goto(x, y)
            # t.ondrag(fun=key)
            t.onclick(fun=key)
            t.onrelease(fun=key2)
        window.update()


pointer_update()
window.mainloop()
s.close()

