import tkinter as tk
import turtle


def pointer_position_wedget(wedget):
    """position of a pointer % widget"""
    coord_W = wedget.winfo_pointerx() - wedget.winfo_rootx()
    coord_H = wedget.winfo_pointery() - wedget.winfo_rooty()
    H = wedget.winfo_height()
    W = wedget.winfo_width()
    Wproportion = coord_W / W
    Hproportion = coord_H / H

    if 1 >= Wproportion >= 0 and 1 >= Hproportion >= 0:
        return Wproportion, Hproportion
    else:
        return -1, -1


def key(event1, event2):
    t.pendown()
    print("left", event1, event2)


window = tk.Tk()
window.title("E-school")
window.geometry("1080x720")

#sandwich pack
master = window
width = 500
height = 500

canvas = tk.Canvas(master=master, width=width, height=height)
canvas.grid(row=1, column=0, sticky="nsew")



t = turtle.RawTurtle(canvas)
# t.hideturtle()
t.speed(0)
t.left(135)
t.penup()
t.pensize(3)
color = "#ff0000"  # red
t.pencolor(color)
while True:
    # turtle pointer folow positon % window
    x, y = pointer_position_wedget(canvas)
    H = canvas.winfo_height()
    W = canvas.winfo_width()
    if x == -1 :
        t.penup()
    else:
        t.goto(x * H - (H / 2), -y * W + (W / 2))
        t.screen._ondrag(item=t.turtle._item, fun=key)
        t.penup()

    """
    turtle.undo()
    """
    # affichage
    window.update()