import os
import tkinter as tk
from tkinter import ttk
import turtle
import fitz
from PIL import Image


def pdf2img():
    pdfName = "Cours arduino + TP.pdf"
    pdfPath = "assets/PdfFiles/"
    savePath = "assets/old/"
    doc = fitz.open(pdfPath + pdfName)
    zoom_x = 2  # horizontal zoom
    zomm_y = 2  # vertical zoom
    mat = fitz.Matrix(zoom_x, zomm_y)
    for i in range(len(doc)):
        page = doc.loadPage(i)  # number of page
        pix = page.getPixmap(matrix=mat)
        output = "outfile.png"
        ch = ' ' + '0' * (len(str(len(doc))) - len(str(i))) + str(i)
        pix.writePNG(savePath + pdfName[:-4] + ch + ".png")


def adapt(test):
    # full screan
    CanvHeight1 = 610
    CanvWidth1 = 1232

    old = "assets/old"
    Currnet = "assets/CurrnetPDF/"

    page_list = list()
    for page in os.listdir(old):
        image = Image.open(old + '/' + page, mode='r')
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
                ch = ' ' + '0' * (2 - len(str(i))) + str(i)
                if test:
                    box = (0, s, Width1, s + CanvHeight1)
                    image_temp = new_image.crop(box)
                    image_temp.save(Currnet + page[:-4] + ch + ".png")
                img_list += [Currnet + page[:-4] + ch + ".png"]
                s += pas
                i += 1

            ch = ' ' + '0' * (2 - len(str(i))) + str(i)
            if test:
                box = (0, Height1 - CanvHeight1, Width1, Height1)
                image_temp = new_image.crop(box)
                image_temp.save(Currnet + page[:-4] + ch + ".png")
            img_list += [Currnet + page[:-4] + ch + ".png"]
        else:
            #new_image.save(Currnet + page)
            img_list += [Currnet + page]
        page_list += [img_list]
    return page_list


def show_frame(page_name):
    """Show a frame for the given page name"""
    """ 
    mainarea.winfo_children()[0].destroy()
    page_name.pack()
    """
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
    t.pendown()


def pen():
    if t.isvisible():
        t.hideturtle()
    else:
        t.showturtle()


def pen_color(item):
    t.pencolor(PenColor.get())


def bg_image(item):
    if item == 'Board':
        t.screen.bgpic(board)
    elif item == 'PDF':
        t.screen.bgpic(CurrentPage)


def back():
    nbr_actions = 50
    for _ in range(nbr_actions):
        t.undo()


def clear_board():
    t.clear()


def page_controle(item):
    """'Up''Down''Next''Previous'"""
    global n, m, CurrentPage

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
    nbr_pages = len(BgImages)
    nbr_divisions = len(BgImages[n % nbr_pages])
    CurrentPage = BgImages[n % nbr_pages][m % nbr_divisions]
    t.screen.bgpic(CurrentPage)


def pdf_images():
    test = True
    return adapt(test)


BgImages = pdf_images()
# create window
# desply_res = (1366, 768)
window = tk.Tk()
window.title("E-school")
# window.geometry("1365x700")
# window.minsize(1080, 480)
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

button3 = tk.Button(side_bar, command=lambda: show_frame(PENDING_CORSES))
image3 = tk.PhotoImage(file="assets/buttons/online-course.png")
button3.config(image=image3)
button3.pack(pady=10)

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

TopBar.grid(row=0, column=0)

CanvHeight = 610  # full screan
CanvWidth = 1232  # full screan
canvas = tk.Canvas(master=LIVE_CORSE, width=CanvWidth, height=CanvHeight)
# canvas.focus_set()  # what does this do ?
canvas.grid(row=1, column=0, sticky="nsew")

SideBar = tk.Frame(LIVE_CORSE)

Up = tk.Button(SideBar, command=lambda: page_controle('Up'))
UpImage = tk.PhotoImage(file='assets/buttons/up.png')
Up.config(image=UpImage)
Up.grid(row=0, column=0)

Down = tk.Button(SideBar, text="Down", command=lambda: page_controle('Down'))
DownImage = tk.PhotoImage(file='assets/buttons/down.png')
Down.config(image=DownImage)
Down.grid(row=1, column=0)
SideBar.grid(row=1, column=1)

BottomBar = tk.Frame(LIVE_CORSE)
Previous = tk.Button(BottomBar, text="Previous", command=lambda: page_controle('Previous'))
PreviousImage = tk.PhotoImage(file='assets/buttons/previous.png')
Previous.config(image=PreviousImage)
Previous.grid(row=0, column=0)

Next = tk.Button(BottomBar, command=lambda: page_controle('Next'))
NextImage = tk.PhotoImage(file='assets/buttons/next.png')
Next.config(image=NextImage)
Next.grid(row=0, column=1)
BottomBar.grid(row=2, column=0)

# Turtle __INIT__
t = turtle.RawTurtle(canvas)
t.screen.setworldcoordinates(0, 1, 1, 0)
canvas.itemconfig(t.screen._bgpic, anchor="nw")
t.speed(0)
t.left(-135)
t.hideturtle()
t.penup()
t.pensize(3)

# 3- Pending_CORSES
PENDING_CORSES = tk.Label(mainarea, text="PENDING_CORSES", font=("courrier", 15), bg='#0C6CAE', fg='white')
PENDING_CORSES.grid(row=0, column=0, sticky="nsew")

# 4- SUPPORT DU COUR
SUPPORT_COUR = tk.Label(mainarea, text="SUPPORT_COUR", font=("courrier", 15), bg='#0C6CAE', fg='white')
SUPPORT_COUR.grid(row=0, column=0, sticky="nsew")

# WELCOME
WELCOME = tk.Label(mainarea, text="welcome", font=("courrier", 15), bg='#0C6CAE', fg='white')
WELCOME.grid(row=0, column=0, sticky="nsew")

# __INIT__
#BgImages = pdf_images()
board = "assets/whiteboard.png"
StartPage = 0
n = StartPage
m = 0
CurrentPage = BgImages[StartPage][m]
t.screen.bgpic(CurrentPage)

while True:
    # if window.focus_get() == LIVE_CORSE:
    # turtle pointer folow positon % window
    x, y = pointer_position_wedget(canvas)
    print()
    if x == -1:
        if t.isdown():
            t.penup()
    else:
        t.goto(x, y)
        t.ondrag(fun=key)
        t.penup()
    # affichage
    window.update()

# affichage backup
#window.mainloop()
