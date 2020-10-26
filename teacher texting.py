import socket
import select
import errno


IP = socket.gethostname()#"127.0.0.1" #
port = 1235
Header_Length= 10

my_username = input("user name : ")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, port))
client_socket.setblocking(False)


while True:
    full_msg = ''
    new_msg = True
    while True:
        msg = client_socket.recv(16)
        if new_msg:
            msglen = int((msg[:Header_Length]))
            new_msg = False
            
        full_msg += msg.decode("utf-8")
        if len(full_msg)- Header_Length == msglen:
            new_msg = True
            print (full_msg)
            full_msg = ''
