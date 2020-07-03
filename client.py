# techwithtim python socket programming tutorial
# create a server and client to communicate

# import relevant packages
import socket

# assign CONSTANT variables
# will need a header size for the message
HEADER = 64
# get a port that should not have a conflict
PORT = 5050
# normal message encoding format
FORMAT = 'utf-8'
# create a message if a client sends then server will close connection
DISCONNECT_MESSAGE = "!DISCONNECT"
# have to hardcode the server address
SERVER = "192.168.1.106"
# give the client the address to connect
ADDR = (SERVER, PORT)

# create a socket for this client to connect to the server using IPv4 and streaming
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect the client socket to the address
client.connect(ADDR)


def send(msg):  # create function to send header and message to server
    # when client enters message encode in format
    message = msg.encode(FORMAT)
    # find the length of the encoded message
    msg_length = len(message)
    # encode the length to send as header
    send_length = str(msg_length).encode(FORMAT)
    # pad the header with enough bytes to be the required header size
    send_length += b' ' * (HEADER - len(send_length))
    # send the header
    client.send(send_length)
    # send the message
    client.send(message)
    print(client.recv(1024).decode(FORMAT))


running = True
while running:
    print("Enter message or 'exit' to exit")
    msg = input()
    if msg == "exit":
        running = False
        send(DISCONNECT_MESSAGE)
    else:
        send(msg)
