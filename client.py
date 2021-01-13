import socket

HEADER = 64
PORT = 6060
SERVER = '192.168.1.102'
FORMAT = 'utf-8'
DISCONNECT_MSG = 'DISCONNECT'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

def send(msg):
    # Convert msg to byte format
    message = msg.encode(FORMAT)
    # Get the length of the msg in bytes
    msg_length = len(message)
    # Encode msg_length as bytes
    send_length = str(msg_length).encode(FORMAT)
    # Pad to 64 bytes
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

connected = True

while connected:
    msg = input()
    if msg.lower() == "disconnect":
        send(DISCONNECT_MSG)
        connected = False
    else:
        send(msg)

