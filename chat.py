"""
    This is the main file in the server projects
    Copyright 2022. All rights reserved. Wiseman Hlophe.
"""


# import statements
import socket
import threading
import sys
import os

# setting the system color
os.system("color 0A")

try:
    host = sys.argv[1]
    port = sys.argv[2]
except IndexError as error:
    host = "10.3.108.25"
    port = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Establishing connection to server...")
try:
    client.connect((host, port))
except socket.error as error:
    print("Connection refused. Try reconnecting again.")
    sys.exit(0)


# receiving the first data from the server that requires name
data = client.recv(4096)
expected = "Enter your name to join the chat: ".encode("utf-8")
while data != expected:
    print(data.decode("utf-8"))
    data = client.recv(4096)

name = input(expected.decode("utf-8"))
client.send(name.encode("utf-8"))


# keep on sending and receiving messages so long the the connection is still maintained
def recvmsg():
    while True:
        try:
            message = client.recv(4096)
            print(message.decode('utf-8'))
        except:
            pass


# function listening from standard input
def chat():
    while True:
        msg = sys.stdin.readline()

        if msg != "" and msg != "exit":
            client.send(msg.encode('utf-8'))
            sys.stdout.write("<You>")
            sys.stdout.write(msg)
            sys.stdout.flush()

        if msg == "exit":
            client.close()
            sys.exit()


chat_thread = threading.Thread(target=chat)
recv_thread = threading.Thread(target=recvmsg)
chat_thread.start()
recv_thread.start()
