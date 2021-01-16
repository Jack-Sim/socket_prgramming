import socket
import threading

HEADER = 64
PORT = 6060
SERVER = '192.168.1.102'
FORMAT = 'utf-8'
DISCONNECT_MSG = 'DISCONNECT'
TOO_MANY_CONNECTIONS_MSG = '[ERROR] Too many players connected'
FIRST_MSG = '[NEW CONNECTION] Welcome to the room'

received_msgs = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

def handle_client(conn, addr):
    # Running concurrently for each client
    if threading.activeCount() - 1 <= 2:
        connected = True
        print(f"[NEW CONNECTION] {addr} connected")
        conn.send(FIRST_MSG.encode(FORMAT))  
    else:
        connected = False
        print(f"[ERROR] Too many connections, {addr} blocked")
        conn.send(TOO_MANY_CONNECTIONS_MSG.encode(FORMAT))

    print(connected)
    
    while connected:
        # Blocking line of code
        # Will not pass until a message is received
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MSG:
                connected = False
            print(f"[{addr}] {msg}")
            
            key_name = f'{addr[0]}:{addr[1]}'

            if key_name in received_msgs.keys():
                received_msgs[key_name].append(msg)
            else:
                received_msgs[key_name] = [msg]

            print(received_msgs)

            conn.send("Msg Received".encode(FORMAT))
    
    conn.close()

def start():
    server.listen()
    while True:
        conn, addr = server.accept() # wait on this line for new connection
        # When new connection occurs pass connection to handle client
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        # How many threads are active in process
        # minus one to account for start thread
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}")

print("[STARTING] server is starting")
start()
