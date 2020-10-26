import socket
import select
import pickle

"""
receive requests from students:
    log in request : verifies name and password, allows log in:
        - send available files for download( documents and previous corses)
        - sends the first up coming live 
    
    download request: send files
    redirect request: send IP address and port  of teacher

receive requests  from teachers:
    log in request : verifies name and password, allows log in
    upload request: resive files
"""

Header_Length = 10
IP = "192.168.1.12"
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()

socket_list = [server_socket]
clients = {}


def receive_message(client_sock):
    try:
        message_header = client_sock.recv(Header_Length)
        if not len(message_header):
            return False
        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_sock.recv(message_length)}

    except:
        return False


print(f'Listening for connections on {IP}:{PORT}...')
while True:
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            if user is False:
                continue
            socket_list.append(client_socket)
            clients[client_socket] = user
            print(f"accept new connection from "
                  f"{client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
        else:
            message = receive_message(notified_socket)
            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user = clients[notified_socket]
            print(f"Recive message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_socket in exception_sockets:
        socket_list.remove(notified_socket)
        del clients[notified_socket]

# while True:
#     clientsocket, adress = server_socket.accept()
#     print(f"connection from {adress} has been established!")
#
#     msg = "welcome to the server mother fucker !"
#     msg = f'{len(msg):<{Header_Length}}' + msg
#     clientsocket.send(bytes(msg,"utf-8"))
#
#     while True:
#         msg = input("send somthing : ")
#         msg = f'{len(msg):<{Header_Length}}' + msg
#         clientsocket.send(bytes(msg,"utf-8"))
