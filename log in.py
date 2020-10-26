import tkinter as tk
from tkinter import ttk
import threading
import socket
import pickle
import errno
import time
import sys
import os


def main():
    def error_manager(err_msg):
        dialog.config(text=err_msg)

    def button_click():
        if authentication():
            window.destroy()
            os.system('teacher_interface.py')

    def on_click(event):
        widget = event.widget
        widget.config(foreground='black')
        if widget.get() == 'user name':
            widget.delete(0, tk.END)
        elif widget.get() == 'Password':
            widget.delete(0, tk.END)
            widget.config(show="*")
        else:
            event.widget.config(foreground='black')

    def on_click2(_):
        if not (show.get()):
            PasswordInput.config(show='')
        else:
            PasswordInput.config(show="*")

    def send_msg(msg):
        bit_msg = (f"{len(msg):<{Header_Size}}" + msg).encode('UTF-8')
        s.send(bit_msg)

    def receive_data():
        """def receave_msg():
            message_header = s.recv(Header_Size)
            message_length = int(message_header.decode('utf-8').strip())
            message = s.recv(message_length).decode('utf-8')
            return message"""

        while True:
            try:
                # Receive our "header" containing username length, it's size is defined and constant
                header = s.recv(Header_Size)
                # If we received no data, server gracefully closed a connection, for example using socket.close()
                # or socket.shutdown(socket.SHUT_RDWR)
                if not len(header):
                    print('Connection closed by the server')
                    return False  # sys.exit()
                # Convert header to int value
                msg_length = int(header.decode('utf-8').strip())
                # Receive and decode username
                message = s.recv(msg_length).decode('utf-8')
                # Now do the same for message (as we received username, we received whole message,
                # there's no need to check if it has any length)
                # return message
                return message
            except IOError as e:
                # This is normal on non blocking connections - when there are no incoming data error is going to be raised
                # Some operating systems will indicate that using AGAIN, and some using EWOULDBLOCK error code
                # We are going to check for both - if one of them - that's expected, means no incoming data,
                # continue as normal
                # If we got different error code - something happened
                if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                    print('Reading error: {}'.format(str(e)))
                    return False  # sys.exit()
                # We just did not receive anything
                continue
            except Exception as e:
                # Any other exception - something happened, exit
                print('Reading error: '.format(str(e)))
                return False  # sys.exit()

    def connect(n):
        try:
            s.connect((IP, port))
            error_manager('connected')
            s.setblocking(False)
            send_msg(User_ID)
        except ConnectionRefusedError as exception:
            print(exception)
            error_manager(str(n + 1) + ' reconnecting . ')
            time.sleep(1)
            error_manager(str(n + 1) + ' reconnecting .. ')
            time.sleep(1)
            error_manager(str(n + 1) + ' reconnecting ... ')
            if n < 9:
                connect(n + 1)
            else:
                error_manager('No connection could be made')

    def authentication():
        def char_test(ch):
            sendable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            for c in ch:
                if not (c in sendable):
                    return True
            return False

        user_name = UserName.get()
        user_password = Password.get()
        if char_test(user_name + user_password):
            error_manager('special characters and white spaces are not allowed')
        elif (user_name and user_password) and (user_name != 'user name' and user_password != 'Password'):
            send_msg(user_name + ' ' + user_password)
            message = receive_data()
            error_manager(message)
            if message == 'access granted':
                return True
        elif not user_name or user_name == 'user name':
            error_manager('user name required')
        elif not user_password or user_password == 'Password':
            error_manager('password required')
        return False

    # create window
    window = tk.Tk()
    window.title("E-school Student ")
    window.wm_minsize(329, 429)
    window.maxsize(329, 429)
    # window.iconbitmap("icone.ico")

    width = 225
    height = 128
    logo = tk.PhotoImage(file="assets/poly.png")  # .zoom(35).subsample(32)
    canvas = tk.Canvas(window, width=width, height=height)
    canvas.create_image(width / 2, height / 2, image=logo)
    canvas.grid(row=0, column=0, columnspan=2, pady=20, padx=50)

    UserName = tk.StringVar(value='user name')
    Password = tk.StringVar(value='Password')
    UserNameInput = ttk.Entry(window, textvariable=UserName,
                              foreground='gray', font=("courrier", 13), width=20)
    UserNameInput.bind("<Button-1>", on_click)
    UserNameInput.bind("<FocusIn>", on_click)
    UserNameInput.grid(row=1, column=0, pady=20, padx=20)

    PasswordInput = ttk.Entry(window, textvariable=Password,
                              foreground='gray', font=("courrier", 13), width=20)
    PasswordInput.bind("<Button-1>", on_click)
    PasswordInput.bind("<FocusIn>", on_click)
    PasswordInput.grid(row=2, column=0, pady=20, padx=20)

    show = tk.IntVar()
    Checkbutton = ttk.Checkbutton(window, text="show", variable=show)
    Checkbutton.bind("<Button-1>", on_click2)
    Checkbutton.grid(row=2, column=1)

    RememberMe = tk.IntVar()
    Checkbutton = ttk.Checkbutton(window, text="remember me", variable=RememberMe)
    Checkbutton.grid(column=0, padx=10)

    button = ttk.Button(window, text="log in", command=lambda: button_click())
    button.grid(column=0, padx=10, pady=30)

    dialog = tk.Label(window, text="connecting ...")
    dialog.grid(sticky='sw', columnspan=2)

    # __INIT__
    # server
    User_ID = 'E-school-test'
    IP = "192.168.1.12"
    port = 1234
    Header_Size = 10
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    t1 = threading.Thread(target=connect, args=(0,), daemon=True)  # stops on program termination
    t1.start()

    window.mainloop()

    # things that happens after closing the window :
    s.close()
    print('done')


main()
