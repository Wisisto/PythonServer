"""
    This is the server file that controls the communication between clients
    Copyright 2022. All rights reserved. Wiseman Hlophe.
"""

# import statements
import socket
import os
import sys
import threading

# setting the system color
os.system("color 0A")

# declaring the host ip address and port number
try:
    host = sys.argv[1]
    port = sys.argv[2]
except IndexError as error:
    host = socket.gethostbyname(socket.gethostname())
    port = 55555

# establish connection and start listening to incoming connections
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    print("Server connection has been successfully established.")
except socket.error as error:
    print(error, " : Server didn't start correctly. Try starting it again.")
    sys.exit(0)


# array variable for storing connections
clients = []
names = []

# now start listening for incoming connections for as long as the server is still up and running
server.listen(100)
print(f"Server has started listening on {host}:{port}")


def clientthread(conn, username):
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')

            if message:
                print(username + "::>" + message)
                message_send = "<" + username + "> " + message
                broadcast(message_send, conn)

            else:
                remove(conn, username)
        except:
            pass


# function for broadcasting message to every connected client
def broadcast(message, sender):
    for each in clients:
        if each != sender:
            try:
                each.send(message.encode('utf-8'))
            except Exception as exc:
                print(exc)
                each.close()


def remove(conn, user):
    if conn in clients:
        msg = user + " has left the chat..."
        broadcast(msg, conn)
        print(msg)
        clients.remove(conn)
    if user in names:
        names.remove(user)


while True:
    connection, address = server.accept()
    clients.append(connection)

    print("Connected to <::> " + address[0] + ":" + str(address[1]))
    connection.send("Connection has been successfully established.".encode("utf-8"))
    connection.send("Enter your name to join the chat: ".encode("utf-8"))

    name = connection.recv(4096).decode("utf-8")
    names.append(name)
    connection.send(f"Server ::> Welcome to Group 22s Server {name}".encode("utf-8"))
    broadcast(f"{name} as joined the chat...", connection)
    print(f"{name} has joined the chat...")

    thread = threading.Thread(target=clientthread, args=(connection, name))
    thread.start()


