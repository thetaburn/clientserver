# techwithtim python socket programming tutorial
# create a server and client to communicate

# import relevant packages
import socket
import threading

# assign CONSTANT variables
# will need a header size for the message
HEADER = 64
# get a port that should not have a conflict
PORT = 5050
# get address of this computer on the local network
SERVER = socket.gethostbyname(socket.gethostname())
# define the server address as the ip and port
ADDR = (SERVER, PORT)
# normal message encoding format
FORMAT = 'utf-8'
# create a message if a client sends then server will close connection
DISCONNECT_MESSAGE = "!DISCONNECT"

# define the server variable as using IPv4 and streaming
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind server var to address and port
server.bind(ADDR)


# need to create a thread for each client connecting to the server
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected. ")

    connected = True
    while connected:
        # first message from client is 64 byte header containing length of next message in utf-8 encoding
        msg_length = conn.recv(HEADER).decode(FORMAT)
        # the initial connection will have null data so make sure msg has data to print
        if msg_length:
            # find the length of the next incoming message
            msg_length = int(msg_length)
            # receive the message containing the info from the client that has the header length
            msg = conn.recv(msg_length).decode(FORMAT)
            # if the message is to disconnect then close the connection
            if msg == DISCONNECT_MESSAGE:
                connected = False
            # otherwise print the message from client
            else:
                print(f"[{addr}] {msg}")
                # respond to client that msg received
                conn.send("message received".encode(FORMAT))
    conn.close()
    print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 2}")

# function to start the server and handle new connections
def start():
    server.listen()
    print(f"[LISTENING] server is listening on {SERVER}")
    while True:
        # return address on new accepted connection send it to new thread
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        # print the number of active connections as all threads minus this thread
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
