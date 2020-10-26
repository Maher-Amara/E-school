import socket
from past.builtins import raw_input


def Main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.connect((host, port))

    filename = raw_input("Filename? -> ")
    if filename != 'q':
        s.send(filename.encode('UTF-8'))
        Bdata = s.recv(1024)
        data = Bdata.decode('UTF-8')
        if data[:6] == 'EXISTS':
            filesize = int(data[6:])
            message = raw_input("File exists, " + str(filesize) + "Bytes, download? (Y/N)? -> ")
            if message == 'Y':
                s.send("OK".encode('UTF-8'))
                f = open('new_' + filename, 'wb')
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print("{0:.2f}".format((totalRecv / float(filesize)) * 100) + "% Done")
                print("Download Complete!")
                f.close()
        else:
            print("File Does Not Exist!")

    s.close()


if __name__ == '__main__':
    Main()
