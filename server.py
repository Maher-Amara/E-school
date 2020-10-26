import socket
import select

Header_Length = 10
IP = socket.gethostname()#"127.0.0.1"
port = 1235

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # what is this ?
server_socket.bind((IP, port))
server_socket.listen()

socket_list = [server_socket]
clients = {}


def recive_message(client_socket):
    try:
        message_header = client_socket.recv(Header_Length)
        if not len(message_header):
            return False
        message_length = int(message_header.decode("utf-8").strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}

    except:
        return False


while True:
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)
    for notified_soket in read_sockets:
        if notified_soket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = recive_message(client_socket)
            if user is False:
                continue
            socket_list.append(client_socket)
            clients[client_socket] = user
            print(
                f"accept new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")
        else:
            message = recive_message(notified_soket)
            if message is False:
                print(f"Closed connection from {clients[notified_soket]['data'].decode('utf-8')}")
                socket_list.remove(notified_soket)
                del clients[notified_soket]
                continue
            user = clients[notified_soket]
            print(f"Recive message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")
            for client_socket in clients:
                if client_socket != notified_soket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])

    for notified_soket in exception_sockets:
        socket_list.remove(notified_soket)
        del clients[notified_soket]

"""
while True:
    clientsocket, adress = server_socket.accept()
    print(f"connection from {adress} has been established!")

    msg = "welcome to the server mother fucker !"
    msg = f'{len(msg):<{Header_Length}}' + msg
    clientsocket.send(bytes(msg,"utf-8"))

    while True:
        msg = input("send somthing : ")
        msg = f'{len(msg):<{Header_Length}}' + msg
        clientsocket.send(bytes(msg,"utf-8"))
"""
