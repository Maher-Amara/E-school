import socket
import select
import threading
import pickle
import queue

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

# __init__
HEADER_LENGTH = 10
IP = "192.168.1.12"
PORT = 1234
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()

# with open("data_base.pickle", 'rb') as fic:
#     ClientsIDs = pickle.load(fic)

ClientsIDs = [
    {'ID': 'E-school-test', 'user name': 'maherDEV', 'password': 'passTest', 'status': 'teacher'},
    {'ID': 'E-school-test1', 'user name': 'maherDEV1', 'password': 'passTest1', 'status': 'student'}
]

print(f'Listening for connections on {IP}:{PORT}...')


def receive_message(client_socket1):
    """Handles message receiving"""
    try:
        # Receive our "header" containing message length, it's size is defined and constant
        message_header = client_socket1.recv(HEADER_LENGTH)
        # If we received no data, client gracefully closed a connection, for example using socket.close() or
        # socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False
        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())
        # Return an object of message header and message data
        return {'header': message_header, 'data': client_socket1.recv(message_length)}

    except:
        # If we are here, client closed connection violently, for example by pressing ctrl+c on his script or just
        # lost his connection socket.close() also invokes socket.shutdown(socket.SHUT_RDWR) what sends information
        # about closing the socket (shutdown read/write) and that's also a cause when we receive an empty message
        return False


def access(user_name, user_password):
    """checks for access permition"""
    for client in ClientsIDs:
        if user_name == client['user name']:
            if user_password == client['password']:
                return True, 'access granted'
            else:
                return False, 'wrong password'
        else:
            return False, 'wrong user name'


def send_msg(client_socket_loc, msg):
    """handles message sending"""
    bit_msg = (f"{len(msg):<{HEADER_LENGTH}}" + msg).encode('UTF-8')
    client_socket_loc.send(bit_msg)


def initialization(temp_client_socket):
    global input_sockets_list, clients
    while True:
        user_data = receive_message(temp_client_socket)
        if user_data is False:
            break
        user_name, user_password = user_data['data'].decode('UTF-8').split()
        access_var = access(user_name, user_password)
        try:
            send_msg(temp_client_socket, access_var[1])
        except socket.error as e:
            print(str(e))
            break
        if access_var[0]:
            # Add accepted socket to select.select() list
            input_sockets_list.append(client_socket)
            # Also save username and username header
            clients[client_socket] = user
            print(
                'Accepted new connection from {}:{}, username: {}'.format(*client_address, user['data'].decode('utf-8'))
            )
            # i need to send json like object to put every thing in place
            break


def main_handler(loc_socket, requesting):
    """get request
    -handles for it and put a response on the queue
    -puts socket on the write list
     - """
    print(loc_socket, 'requesting', requesting)


# List of sockets for select.select()
input_sockets_list = [server_socket]
output_socket_list = []

# List of connected clients - socket as a key, user header and name as data
clients = {}
message_queues = {}

while True:

    # Calls Unix select() system call or Windows select() WinSock call with three parameters: - rlist - sockets to be
    # monitored for incoming data - wlist - sockets for data to be send to (checks if for example buffers are not
    # full and socket is ready to send some data) - xlist - sockets to be monitored for exceptions (we want to
    # monitor all sockets for errors, so we can use rlist) Returns lists: - reading - sockets we received some data
    # on (that way we don't have to check sockets manually) - writing - sockets ready for data to be send thru them -
    # errors  - sockets with some exceptions This is a blocking call, code execution will "wait" here and "get"
    # notified in case any action should be taken
    read_sockets, write_sockets, exception_sockets = select.select(input_sockets_list, output_socket_list,
                                                                   input_sockets_list)

    # Iterate over notified sockets
    for notified_socket in read_sockets:
        # If notified socket is a server socket - new connection, accept it
        if notified_socket == server_socket:
            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            # The other returned object is ip/port set
            client_socket, client_address = server_socket.accept()
            # Client should send his name right away, receive it (ID , and status)
            user = receive_message(client_socket)
            # If False - client disconnected before he sent his name
            if user is False:
                continue
            t = threading.Thread(target=initialization, args=(client_socket,), daemon=True)
            t.start()
        # Else existing socket is sending a message
        else:
            # Receive message
            request = receive_message(notified_socket)
            # If False, client disconnected, cleanup
            if request is False:
                print('Closed connection from: {}'.format(clients[notified_socket]['data'].decode('utf-8')))
                input_sockets_list.remove(notified_socket)
                del clients[notified_socket]
                del message_queues[notified_socket]
                if notified_socket in output_socket_list:
                    output_socket_list.remove(notified_socket)
                # notified_socket.close()
                continue
            # Get user by notified socket, so we will know who sent the message
            user = clients[notified_socket]
            print(f'Received request from {user["data"].decode("utf-8")}: {request["data"].decode("utf-8")}')
            # handle for that request
            main_handler(socket, request)

    # Iterate over write_sockets
    for notified_socket in write_sockets:
        pass

    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:
        # Remove from list for socket.socket()
        input_sockets_list.remove(notified_socket)
        # Remove from our list of users
        del clients[notified_socket]
